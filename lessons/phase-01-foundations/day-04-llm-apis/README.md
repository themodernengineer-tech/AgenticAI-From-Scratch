# Day 4 — LLM APIs, Model Calls, and Latency

## What We Are Learning

An AI application needs a way to send information to a language model and receive its response. That connection is commonly provided by an **application programming interface**, or API. In this lesson, we’ll learn the parts of a model request, then extend our initial Gemini call to limit its response length and measure how long it takes.

This is our first step from “the API call works” to “we can describe and observe what our application sends and receives.” We’ll build on it in later lessons with tools, agent loops, memory, and evaluation.

## Learning Objectives

By the end of this lesson, we should be able to:

- Explain the roles of an application, SDK, API, and model.
- Identify the model and input in a Gemini request.
- Explain how an input string relates to role-based messages.
- Describe generation settings and output-token limits.
- Measure the elapsed time of an API request.
- Recognize common API error categories and where to investigate them.
- Explain why usage, quota, privacy, and cost should be considered.

## 1. How an LLM API Call Works

An **LLM API** provides a way for one program to request a response from a language model hosted by a provider. Our Python application sends a request over the network; the provider processes it and returns a response. The model does not run inside our Python file just because we use the SDK.

The parts have different jobs:

| Part | What it does in this project |
|---|---|
| **Application** | Our Python program in `main.py`. It decides what to ask and what to do with the response. |
| **SDK** | The `google-genai` Python package. It gives us Python methods for communicating with Gemini. |
| **API** | The provider’s request-and-response interface. |
| **Model** | The selected language model that generates a response. |

The request path is:

```text
Python application → Gemini SDK → Gemini API → selected model
Python application ← Gemini SDK ← Gemini API ← model response
```

The SDK handles communication details for us. We still need to choose a model, provide suitable input, handle errors, and decide what our application should do with the response.

## 2. Model, Input, and Response

A **model ID** names the model that should process a request. Our existing code uses `gemini-3.5-flash-lite`. The model provider controls which model IDs are available, their capabilities, and their usage limits. Model names and availability can change, so check the provider’s current model documentation when starting a new project.

**Input** is the information we send to the model. In our first call, the input is a plain text prompt:

```python
input="In one sentence, explain what an AI agent is."
```

The model returns an **output** containing its generated response. Our code prints that output with:

```python
print(response.output_text)
```

A successful response tells us that this particular request completed. It does not prove the model is always correct or that every future request will succeed.

## 3. Inputs and Role-Based Messages

Many chat APIs represent a conversation as a sequence of messages with roles. A role identifies who supplied each message. Common roles include `user` for a request from a person and `assistant` for a model response. Some interfaces also provide a system-level instruction that sets behavior or context.

Our current Interactions API call uses a plain string in `input`, which is suitable for one simple request. It is not a complete multi-turn conversation history. Later, when we build conversational behavior, we’ll study how the API represents turns, roles, and continuing state.

The concepts of a role and an API field name should not be confused: different APIs and SDKs can represent similar conversation concepts with different request formats.

## 4. Generation Settings and Token Limits

**Generation settings** are options that control how the model responds. One useful setting is `max_output_tokens`, which limits the number of tokens the model may generate for its response. A token is a unit of text processing; it may represent a word, part of a word, punctuation, or another text unit.

A token limit is not a word limit. The exact relationship between tokens and words varies with the text. A lower output limit can help keep a response short, but it may also cut off an answer before it is complete.

**Temperature** is a commonly discussed setting that influences variation in generated responses. Its behavior and recommended values can depend on the model. We’ll leave it at the model’s default in this experiment rather than change settings without a specific reason.

## 5. Latency

**Latency** is the elapsed time between starting a request and receiving its response. The time can vary because of the network, provider load, the selected model, input size, output size, and model processing.

We’ll measure elapsed time in our Python program using `time.perf_counter()`. The measurement is useful for comparing repeated runs under similar conditions, but one run is not enough to make a reliable performance claim.

## 6. Usage, Quota, Cost, and Privacy

Model requests consume resources. Providers may measure usage using input and output tokens and apply rate limits or quotas. Whether a request is free, how much quota is available, and whether billing applies depend on the provider, model, account, and current plan. We will not assume that “free tier” means unlimited usage; check the current Google AI Studio usage and plan details.

For this learning project, keep requests short and use only the access available to your account. Do not enable paid billing just to run this lesson. If the available quota is exhausted, stop and review the account’s limits rather than repeatedly retrying.

Also consider what information is sent to an external model provider. Do not include passwords, API keys, private records, or other sensitive information in prompts. Review the provider’s current data-use terms before using real personal or business data.

## 7. Common API Errors

An API error means the request did not complete as expected. The status code and error message help identify what to investigate.

| Error category | Common interpretation | First checks |
|---|---|---|
| **400 — Bad Request** | The request may contain an invalid field, unsupported value, or malformed input. | Check the request fields and model documentation. |
| **401 or 403 — Authentication or permission** | The key may be missing, invalid, restricted, or unauthorized for the requested API or model. | Check local key configuration and provider permissions. Never print or share the key. |
| **429 — Rate limit or quota** | The request may have exceeded a rate limit or available quota. | Check account usage and limits; wait before retrying if it is a temporary rate limit. |
| **5xx — Provider error** | The service may be experiencing a temporary problem. | Check provider status and retry later if appropriate. |

A key-loading check only confirms that Python can read a value from the environment. It does not confirm that the provider accepts the key. Also, retrying an invalid request does not fix the request, and retrying after quota exhaustion may not help.

## 8. Our Experiment

We will extend the existing smoke test to:

1. Send one prompt to Gemini.
2. Set a maximum output-token limit.
3. Measure how long the request takes.
4. Print the response and elapsed time.

The runnable code remains in:

```text
lessons/phase-01-foundations/day-04-llm-apis/experiment.py
```

We will update that file in the next step. The planned request will use this structure:

```python
response = client.interactions.create(
    model="gemini-3.5-flash-lite",
    input="In one sentence, explain what an AI agent is.",
    generation_config={"max_output_tokens": 120},
)
```

The timing will be measured around the request:

```python
start_time = time.perf_counter()

response = client.interactions.create(...)

elapsed_seconds = time.perf_counter() - start_time
```

The full runnable code will be in `main.py`; we’ll avoid maintaining a second copy of the program in this README.

## 9. Run the Experiment

From the project root in the VS Code PowerShell terminal, run:

```powershell
uv run python lessons/phase-01-foundations/day-04-llm-apis/experiment.py
```

A successful run should print a Gemini response and a latency value in seconds. The response text and timing may vary between runs.


## 10. Troubleshooting

| Symptom | What to check |
|---|---|
| Python reports a missing module | From the project root, run `uv sync` and confirm the dependency is in `pyproject.toml`. |
| The program cannot find the API key | Confirm `.env` is in the project root, `load_dotenv()` runs before client creation, and the variable is named `GEMINI_API_KEY`. |
| Authentication or permission error | Check the key and its API permissions in the provider console. Do not share the key. |
| Rate-limit or quota error | Check account usage and limits. Wait if the provider indicates a temporary rate limit. |
| The request returns a model or parameter error | Confirm the model ID and request fields against the current Gemini API documentation. |
| The call takes longer than expected | Record the time and try another run later; one measurement can be affected by network and provider conditions. |


## Experiment Results

- **Model:** `gemini-3.5-flash-lite`
- **Maximum output tokens:** `120`
- **Response received:** Yes
- **Latency:** `2.76 seconds`
- **Observation:** The request returned a complete sentence. The measured latency includes the time my program waited for the API response and may vary between runs.
- **Troubleshooting:** No errors encountered.

## Day 4 Recap

We learned that our Python application uses an SDK to send a request through an API to a selected model. The request contains input and can include generation settings. We distinguished a simple input string from a role-based conversation, learned what an output-token limit does, and identified latency, usage, quota, cost, privacy, and common error categories as engineering concerns.

## Assessment

Answer these questions in your own words:

1. What is the difference between the model, API, SDK, and application in our project?
2. What does `input` represent in our current Gemini call?
3. How is a plain input string different from a multi-turn conversation represented by role-based messages?
4. What does `max_output_tokens` limit, and why is it not the same as a word limit?
5. What does our latency measurement tell us? Why should we not draw conclusions from only one run?
6. What does a successful key-loading check prove, and what does it not prove?
7. How would you investigate a 429 error differently from a 400 error?








