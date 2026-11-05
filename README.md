# LearnX LLM API call

## Install

From the project root:

```powershell
python -m pip install -r person_c\requirements.txt
```

## Configure Gemini

Copy `.env.example` to `.env` and set `GEMINI_API_KEY`. The optional
`GEMINI_MODEL_NAME` defaults to `gemini-3.6-flash`. Keep `.env` private and
never commit API keys.

## Start the API

From the project root:

```powershell
uvicorn person_c.api:app --reload
```

Interactive API documentation: <http://127.0.0.1:8000/docs>

## Check health

```powershell
curl.exe http://127.0.0.1:8000/health
```

## Analyze a submission

```powershell
curl.exe -X POST http://127.0.0.1:8000/analyze `
  -H "Content-Type: application/json" `
  -d '{"student_code":"while True:\n    pass","test_code":"print(\"Testing\")","skill":"SKL-02","hint_level":"L1","timeout":3}'
```

The response contains `runner_result`, `diagnosis`, and `hint`. The optional
`POST /diagnose` endpoint returns only the runner result and diagnosis.

## Run tests

```powershell
python -m pytest person_c\tests
```

Gemini calls are mocked in API tests; a live API key is not needed to run tests.

## Security limitation

The current API executes submitted code using the existing subprocess runner.
A subprocess timeout alone does not make arbitrary code execution safe. Do not
expose this API publicly without appropriate access controls. Production use
requires an isolated sandbox, resource limits, restricted filesystem/network
access, and other deployment-specific protections.
