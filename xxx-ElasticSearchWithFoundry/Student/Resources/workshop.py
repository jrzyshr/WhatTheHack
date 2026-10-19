"""Shared plumbing for the Context Quest authoring draft; not live-validated."""

import json
import os
import re
import time
from collections import Counter
from pathlib import Path
from urllib.parse import quote, urlparse

import requests
from azure.ai.projects import AIProjectClient
from azure.identity import AzureCliCredential
from dotenv import load_dotenv
from elasticsearch import Elasticsearch, helpers
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

ROOT = Path(__file__).resolve().parent


def configure():
    load_dotenv(ROOT / ".env", override=True)
    workshop_id()


def required(name):
    value = os.environ.get(name, "").strip()
    if not value:
        raise ValueError(f"Configure {name} in the local .env file.")
    return value


def workshop_id():
    value = required("WORKSHOP_ID")
    if not re.fullmatch(r"[a-z][a-z0-9-]{3,23}", value):
        raise ValueError("WORKSHOP_ID must be 4-24 lowercase letters/digits/hyphens, starting with a letter.")
    return value


def https_url(name):
    value = required(name).rstrip("/")
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
        raise ValueError(f"{name} must be an HTTPS URL without embedded credentials.")
    if parsed.query or parsed.fragment:
        raise ValueError(f"{name} must not contain a query string or fragment.")
    return value


def kibana_base():
    base = https_url("KIBANA_URL")
    space = os.environ.get("KIBANA_SPACE_ID", "default").strip()
    if not space:
        raise ValueError("KIBANA_SPACE_ID must be default or a specific space ID.")
    return base if space == "default" else f"{base}/s/{quote(space, safe='')}"


def mcp_url():
    return f"{kibana_base()}/api/agent_builder/mcp"


def es_client():
    return Elasticsearch(
        https_url("ELASTICSEARCH_URL"),
        api_key=required("ELASTIC_API_KEY"),
        request_timeout=60,
        max_retries=2,
        retry_on_timeout=True,
    )


def kibana_request(method, path, body=None):
    response = requests.request(
        method,
        f"{kibana_base()}{path}",
        headers={
            "Authorization": f"ApiKey {required('ELASTIC_API_KEY')}",
            "kbn-xsrf": "true",
            "elastic-api-version": "2023-10-31",
        },
        json=body,
        timeout=60,
    )
    response.raise_for_status()
    return response.json()


def read_json(relative_path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def save_json(filename, value):
    if Path(filename).name != filename or not filename.endswith(".json"):
        raise ValueError("Evidence files must be plain .json filenames inside outputs/.")
    destination = ROOT / "outputs" / filename
    destination.parent.mkdir(exist_ok=True)
    destination.write_text(json.dumps(value, indent=2), encoding="utf-8")
    destination.chmod(0o600)
    return destination


def source_names(include_safety=False):
    suffixes = ["accounts", "tickets", "products", "policies"]
    if include_safety:
        suffixes.append("safety")
    return [f"cq-{workshop_id()}-{suffix}" for suffix in suffixes]


def seed_data(safety=False):
    dataset = read_json("data/safety.json" if safety else "data/sources.json")
    results = []
    with es_client() as client:
        for source in dataset["sources"]:
            name = f"cq-{workshop_id()}-{source['suffix']}"
            ownership = {"workshop_id": workshop_id(), "dataset_version": dataset["version"]}
            if client.indices.exists(index=name):
                metadata = client.indices.get_mapping(index=name)[name]["mappings"].get("_meta", {})
                if any(metadata.get(key) != value for key, value in ownership.items()):
                    raise RuntimeError(f"Refusing to overwrite unowned or different-version index: {name}")
            else:
                client.indices.create(
                    index=name,
                    mappings={
                        "_meta": {**ownership, "description": source["description"]},
                        "properties": {
                            "record_id": {"type": "keyword"},
                            "title": {"type": "text"},
                            "body": {"type": "text"},
                            **source["fields"],
                        },
                    },
                )
            helpers.bulk(
                client,
                (
                    {"_index": name, "_id": doc["record_id"], "_source": doc}
                    for doc in source["documents"]
                ),
                refresh="wait_for",
            )
            results.append({
                "index": name,
                "bundled_records": len(source["documents"]),
                "actual_records": client.count(index=name)["count"],
            })
    return results


async def discover_tools(profile):
    if profile not in ("baseline", "optimus"):
        raise ValueError("Profile must be baseline or optimus.")
    key = required(f"ELASTIC_{profile.upper()}_API_KEY")
    async with streamablehttp_client(
        mcp_url(), headers={"Authorization": f"ApiKey {key}"}
    ) as (read_stream, write_stream, _):
        async with ClientSession(read_stream, write_stream) as session:
            await session.initialize()
            tools = []
            cursor = None
            for _ in range(20):
                page = await session.list_tools(cursor=cursor)
                tools.extend(tool.model_dump(mode="json") for tool in page.tools)
                cursor = page.nextCursor
                if not cursor:
                    return tools
            raise RuntimeError("MCP tool pagination exceeded the workshop limit.")


def tool_names(profile):
    if profile not in ("baseline", "optimus"):
        raise ValueError("Profile must be baseline or optimus.")
    names = [
        required("MCP_LIST_INDICES_TOOL"),
        required("MCP_MAPPING_TOOL"),
        required("MCP_ESQL_TOOL"),
    ]
    if len(set(names)) != 3:
        raise ValueError("Choose three distinct discovery/mapping/source-query tools.")
    if profile == "optimus":
        context = [name.strip() for name in required("MCP_CONTEXT_TOOLS").split(",") if name.strip()]
        if not context:
            raise ValueError("No native Context Engine MCP tools configured.")
        if set(context).intersection(names):
            raise ValueError("Native context tools must be distinct from ordinary source-query tools.")
        names.extend(context)
    return list(dict.fromkeys(names))


def foundry_clients():
    project = AIProjectClient(
        endpoint=https_url("AZURE_AI_PROJECT_ENDPOINT"),
        credential=AzureCliCredential(),
    )
    return project, project.get_openai_client()


def base_prompt():
    return (
        "You are Northstar Support's read-only support assistant. "
        f"Use only these source indices: {', '.join(source_names())}. "
        "Discover sources as needed using the provided tools; do not guess facts. "
        "Use ES|QL for source retrieval, select only necessary fields including record_id, "
        "and limit each retrieval to at most five records. "
        "Cite source index names and record_id values for factual claims. "
        "Explain missing evidence and unsupported requests. Do not perform writes."
    )


def optimus_prompt():
    description_file = ROOT / required("ELASTIC_AI_INDEX_DESCRIPTION_FILE")
    if not description_file.is_file():
        raise ValueError("Save the actual native AI Index description in Challenge 02 first.")
    return (
        base_prompt()
        + "\nBefore source discovery, retrieve relevant KIs using the native Context Engine tools "
        f"for AI Index {required('ELASTIC_AI_INDEX_ID')}. Follow its verified query guidance "
        "when useful, then retrieve current source facts when needed. "
        "An AI Index contains reusable context, not merged live records. "
        "AI Index description from setup:\n"
        + description_file.read_text(encoding="utf-8")
    )


def agent_reference(agent):
    return {
        "agent_reference": {
            "name": agent.name,
            "version": agent.version,
            "type": "agent_reference",
        }
    }


def remember_agent(agent, label):
    return save_json(f"{label}-agent.json", {
        "workshop_id": workshop_id(),
        "project_endpoint": https_url("AZURE_AI_PROJECT_ENDPOINT"),
        "name": agent.name,
        "version": agent.version,
    })


def run_agent(client, agent, question, allowed_tools):
    """Keep every response/usage record, including manual approval continuations."""
    conversation = client.conversations.create()
    responses = []
    started = time.monotonic()
    response = client.responses.create(
        conversation=conversation.id,
        input=question,
        max_output_tokens=2500,
        max_tool_calls=12,
        parallel_tool_calls=False,
        extra_body=agent_reference(agent),
    )
    for continuation in range(12):
        payload = response.model_dump(mode="json")
        responses.append(payload)
        save_json(f"inflight-{conversation.id}.json", {
            "workshop_id": workshop_id(),
            "agent": {"name": agent.name, "version": agent.version},
            "query": question,
            "conversation_id": conversation.id,
            "responses": responses,
        })
        approvals = []
        for item in payload.get("output", []):
            if item["type"] == "mcp_call" and (item.get("error") or item.get("status") == "failed"):
                raise RuntimeError(f"Elastic MCP call failed. Inspect response {response.id} in Foundry.")
            if item["type"] == "mcp_approval_request":
                print("Review read-only MCP request:", item.get("server_label"), item.get("name"))
                print(item.get("arguments"))
                if item.get("server_label") != "elastic" or item.get("name") not in allowed_tools:
                    raise RuntimeError("Unexpected server/tool; no approval submitted.")
                approve = input("Approve this exact read-only call? Type yes: ").strip() == "yes"
                approvals.append({
                    "type": "mcp_approval_response",
                    "approval_request_id": item["id"],
                    "approve": approve,
                })
        if not approvals:
            if response.status != "completed" or not response.output_text:
                raise RuntimeError(f"Run did not produce a completed answer: {response.id}, {response.status}")
            return {
                "workshop_id": workshop_id(),
                "agent": {"name": agent.name, "version": agent.version},
                "configured_model_deployment": required("AZURE_AI_MODEL_DEPLOYMENT_NAME"),
                "allowed_tools": list(allowed_tools),
                "project_endpoint": https_url("AZURE_AI_PROJECT_ENDPOINT"),
                "query": question,
                "conversation_id": conversation.id,
                "response": response.output_text,
                "responses": responses,
                "latency_seconds": round(time.monotonic() - started, 3),
                "latency_includes_manual_approval": True,
                "measurement_scope": "Foundry response usage only; excludes KI generation and Elastic-side models",
            }
        if continuation == 11:
            raise RuntimeError("Approval continuation limit reached; inspect the saved inflight trace.")
        response = client.responses.create(
            input=approvals,
            previous_response_id=response.id,
            max_output_tokens=2500,
            max_tool_calls=12,
            parallel_tool_calls=False,
            extra_body=agent_reference(agent),
        )
    raise RuntimeError("Approval continuation limit reached; stop and inspect the trace.")


def mcp_calls(run):
    calls = {}
    for response in run["responses"]:
        for item in response.get("output", []):
            if item["type"] == "mcp_call":
                calls[item["id"]] = item
    return list(calls.values())


def summarize(run):
    responses = {response["id"]: response for response in run["responses"]}.values()
    usages = [response.get("usage") for response in responses]
    metrics = {}
    for field in ("input_tokens", "output_tokens", "total_tokens"):
        values = [usage.get(field) if usage else None for usage in usages]
        metrics[field] = sum(values) if values and all(value is not None for value in values) else None
    cached = [
        (usage.get("input_tokens_details") or {}).get("cached_tokens") if usage else None
        for usage in usages
    ]
    metrics["cached_input_tokens"] = (
        sum(cached) if cached and all(value is not None for value in cached) else None
    )
    context = {name.strip() for name in os.environ.get("MCP_CONTEXT_TOOLS", "").split(",") if name.strip()}
    discovery = {os.environ.get("MCP_LIST_INDICES_TOOL"), os.environ.get("MCP_MAPPING_TOOL")}
    categories = Counter()
    for call in mcp_calls(run):
        name = call.get("name")
        category = "context" if name in context else "discovery" if name in discovery else "source"
        categories[category] += 1
    return {
        "agent": run["agent"]["name"],
        **metrics,
        "tool_calls": len(mcp_calls(run)),
        "discovery_calls": categories["discovery"],
        "context_calls": categories["context"],
        "source_calls": categories["source"],
        "elapsed_including_approval_seconds": run["latency_seconds"],
    }


def trace(run):
    return [
        {"name": item.get("name"), "arguments": item.get("arguments"),
         "output": item.get("output"), "error": item.get("error")}
        for item in mcp_calls(run)
    ]


def retrieved_records(value):
    """Recognize document rows, including ES|QL tables inside MCP text envelopes."""
    if isinstance(value, str):
        try:
            decoded = json.loads(value)
        except json.JSONDecodeError:
            return
        yield from retrieved_records(decoded)
    elif isinstance(value, list):
        for child in value:
            yield from retrieved_records(child)
    elif isinstance(value, dict):
        if isinstance(value.get("record_id"), str) and isinstance(value.get("body"), str):
            yield value
        columns, rows = value.get("columns"), value.get("values")
        if isinstance(columns, list) and isinstance(rows, list):
            names = [column.get("name") if isinstance(column, dict) else column for column in columns]
            if "record_id" in names and "body" in names:
                for row in rows:
                    if isinstance(row, list) and len(row) == len(names):
                        yield dict(zip(names, row))
        for child in value.values():
            yield from retrieved_records(child)


def require_retrieved(run, record_id):
    outputs = [call.get("output") for call in mcp_calls(run) if not call.get("error")]
    records = [record for output in outputs for record in retrieved_records(output)]
    if not any(record["record_id"] == record_id and record["body"] for record in records):
        raise RuntimeError(
            f"No structured record_id/body evidence for {record_id}. "
            "Inspect the MCP output format and retrieve those fields; a query echo is not evidence."
        )
    return "\n".join(output if isinstance(output, str) else json.dumps(output) for output in outputs)


def evaluation_row(run, record_id):
    context = require_retrieved(run, record_id)
    messages = [{"role": "user", "content": run["query"]}]
    for call in mcp_calls(run):
        messages.append({
            "role": "assistant",
            "content": [{
                "type": "tool_call",
                "tool_call_id": call["id"],
                "name": call["name"],
                "arguments": json.loads(call["arguments"]),
            }],
        })
        messages.append({
            "role": "tool",
            "tool_call_id": call["id"],
            "content": [{"type": "tool_result", "tool_result": {"text": call.get("output")}}],
        })
    messages.append({"role": "assistant", "content": run["response"]})
    return {
        "query": run["query"], "context": context, "response": run["response"],
        "messages": messages, "record_id": record_id, "agent": run["agent"],
        "response_ids": [response["id"] for response in run["responses"]],
    }


def delete_owned_sources(confirmation):
    if confirmation != f"DELETE {workshop_id()}":
        raise ValueError("Deletion confirmation does not match.")
    deleted = []
    with es_client() as client:
        for name in source_names(include_safety=True):
            if not client.indices.exists(index=name):
                continue
            metadata = client.indices.get_mapping(index=name)[name]["mappings"].get("_meta", {})
            if metadata.get("workshop_id") != workshop_id():
                raise RuntimeError(f"Refusing to delete unowned index: {name}")
            client.indices.delete(index=name)
            deleted.append(name)
    return deleted
