# divops-tarot
devops tarot for divination or fortune-telling

[Frontend] → [Spring Boot (Java)] → HTTP Request → [Python AI Service] → LangChain Inference → Return Result

```ai-service/
├── app/
│   ├── rag_engine.py              # AI reasoning
│   ├── main.py                    # FastAPI HTTP interface
│   └── tarot_prompt_template.txt  # Prompt word template
├── requirements.txt
├── docker-compose.yml
├── Dockerfile
└── .env                           # Store OpenAI Key