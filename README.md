# OpsPilot AI - Agentic CloudOps Incident Diagnosis Copilot

OpsPilot AI is an agentic CloudOps assistant built with LangGraph, Streamlit, Docker, and AWS ECS Fargate. The application diagnoses cloud and container deployment incidents by routing issues through specialized diagnostic agents, generating root-cause analysis, recommending fixes, evaluating response quality, and producing an incident report.

## Project Objective

The goal of this project is to demonstrate an end-to-end production-style Agentic AI system for CloudOps incident triage and remediation guidance.

Instead of using a single LLM prompt, OpsPilot AI models incident diagnosis as a multi-step agentic workflow with:

- Conditional routing
- Specialized diagnostic nodes
- Root-cause reasoning
- Fix generation
- Evaluation loop
- Final incident reporting
- Containerized AWS Fargate deployment

## System Architecture

```text
User
 |
 v
Streamlit UI
 |
 v
LangGraph Workflow
 |
 +--> Router Node
 |       |
 |       +--> ECS Diagnostics Node
 |       +--> Generic Planner Node
 |       +--> Log Analyzer Node
 |
 v
Root Cause Node
 |
 v
Fix Generator Node
 |
 v
Evaluator Node
 |
 +--> Pass -> Reporter Node
 +--> Fail -> Retry Root Cause Analysis
 |
 v
Final Incident Report
 |
 v
Docker -> ECR -> ECS Fargate -> CloudWatch Logs
```

## Key Features

- Agentic workflow orchestration using LangGraph
- Conditional routing based on incident category
- Specialized ECS/Fargate diagnostic path
- CloudOps-focused root-cause analysis
- Fix recommendation generation
- Response evaluation and retry logic
- Streamlit-based interactive UI
- Dockerized application
- AWS ECS Fargate deployment
- CloudWatch logging support

## Tech Stack

| Layer | Technology |
| --- | --- |
| Frontend | Streamlit |
| Agent Framework | LangGraph |
| LLM Integration | LangChain / OpenAI |
| Language | Python |
| Containerization | Docker |
| Image Registry | Amazon ECR |
| Deployment | Amazon ECS Fargate |
| Logs / Monitoring | Amazon CloudWatch |
| Secrets | Environment variables / AWS task definition secrets |

## Project Structure

```text
opspilot-ai/
|
+-- app.py
+-- requirements.txt
+-- Dockerfile
+-- .dockerignore
+-- .gitignore
+-- .env.example
|
+-- src/
|   +-- state.py
|   +-- llm.py
|   +-- workflow.py
|
+-- agents/
|   +-- router.py
|   +-- planner.py
|   +-- log_analyzer.py
|   +-- ecs_diagnostics.py
|   +-- root_cause.py
|   +-- fix_generator.py
|   +-- evaluator.py
|   +-- reporter.py
|
+-- deployment/
    +-- task-definition-template.json
```

## LangGraph Workflow

The core workflow is implemented as a stateful graph. Each node receives a shared state object, performs one responsibility, and returns partial updates to the state.

| Node | Responsibility |
| --- | --- |
| Router Node | Classifies the incident and chooses the workflow path |
| Planner Node | Generates an investigation plan |
| ECS Diagnostics Node | Performs ECS/Fargate-specific troubleshooting |
| Log Analyzer Node | Extracts key signals from logs |
| Root Cause Node | Identifies likely cause and supporting evidence |
| Fix Generator Node | Recommends practical remediation steps |
| Evaluator Node | Checks quality, grounding, and hallucination risk |
| Reporter Node | Produces final incident report |

## Example Use Case

Input:

```text
ECS Fargate task is running but the Streamlit app is not loading.
Logs show connection refused on port 8501.
```

Expected workflow:

```text
router_node
-> ecs_diagnostics_node
-> root_cause_node
-> fix_generator_node
-> evaluator_node
-> reporter_node
```

Output includes:

- Incident type
- Diagnostic summary
- Root cause
- Suggested fix
- Evaluation feedback
- Final incident report
- Execution trace

## Local Setup

### 1. Clone the Repository

```bash
git clone https://github.com/<your-username>/cloud-ops-incident-multiagent-llmops.git
cd cloud-ops-incident-multiagent-llmops
```

### 2. Create Virtual Environment

```bash
python -m venv venv
```

Activate on Windows:

```powershell
.\venv\Scripts\activate
```

Activate on macOS/Linux:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key_here
OPENAI_MODEL=gpt-4o-mini
```

Do not commit `.env` to GitHub.

### 5. Run Locally

```bash
streamlit run app.py
```

## Docker Deployment

Build the Docker image:

```bash
docker build -t opspilot-ai .
```

Run the Docker container locally:

```bash
docker run -p 8501:8501 --env-file .env opspilot-ai
```

Open:

```text
http://localhost:8501
```

## AWS Deployment Overview

The application can be deployed using:

```text
Docker Image
-> Amazon ECR
-> ECS Task Definition
-> ECS Fargate Service
-> Public IP or Load Balancer
-> CloudWatch Logs
```

| AWS Component | Purpose |
| --- | --- |
| ECR | Stores Docker image |
| ECS Cluster | Logical container orchestration environment |
| Fargate | Serverless container runtime |
| Task Definition | Blueprint for container configuration |
| ECS Service | Keeps desired number of tasks running |
| Security Group | Controls inbound/outbound traffic |
| CloudWatch Logs | Stores application logs |

## Important Deployment Notes

- Streamlit must bind to `0.0.0.0`.
- Container port `8501` must be exposed.
- Security groups must allow inbound traffic on port `8501` only where appropriate.
- ECS task execution role must have permissions for ECR image pulls and CloudWatch logs.
- CloudWatch log group must exist before task startup unless your deployment creates it.
- API keys should never be hardcoded in source code or task definition JSON.
- Prefer AWS Secrets Manager or SSM Parameter Store for production secrets.

## Sample Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

## Monitoring

Useful AWS CLI commands:

```bash
aws ecs describe-services \
  --cluster opspilot-cluster \
  --services opspilot-service \
  --region us-east-1
```

```bash
aws logs tail /ecs/opspilot --follow --region us-east-1
```

```bash
aws cloudwatch get-metric-statistics \
  --namespace AWS/ECS \
  --metric-name CPUUtilization \
  --dimensions Name=ClusterName,Value=opspilot-cluster Name=ServiceName,Value=opspilot-service \
  --period 300 \
  --statistics Average \
  --region us-east-1
```

## Engineering Highlights

This project demonstrates:

- Agentic AI system design
- State-based workflow orchestration
- Conditional graph execution
- Specialized diagnostic agents
- LLM evaluation loop
- Cloud-native deployment
- Containerization
- AWS ECS/Fargate operations
- Observability using CloudWatch

## Future Enhancements

- Add RAG over AWS documentation and internal runbooks
- Add CloudWatch log ingestion through AWS APIs
- Add auto-remediation with human approval gates
- Add persistent incident memory
- Add ALB, HTTPS, and custom domain
- Add authentication
- Add LangSmith tracing
- Add CloudWatch dashboard
- Add real-world incident dataset for evaluation

## Security Considerations

- Do not commit `.env`.
- Do not expose API keys in GitHub.
- Prefer AWS Secrets Manager for production secrets.
- Use least-privilege IAM policies.
- Avoid automated infrastructure changes without approval.
- Restrict security group rules in production.
- Keep real AWS account IDs, ARNs, and repository URLs out of public examples unless intentionally published.


## License

This project is intended for educational and portfolio purposes.
