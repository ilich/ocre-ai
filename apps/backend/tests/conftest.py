import os

os.environ.setdefault("MONGODB_URI", "mongodb://localhost:27017")
os.environ.setdefault("MONGODB_DATABASE", "ocre-ai-test")
os.environ.setdefault("SECRET_KEY", "test-secret-key-with-at-least-32-bytes")
os.environ.setdefault("PUBLIC_URL", "http://localhost:8000")
os.environ.setdefault("EMAIL_FROM", "noreply@example.com")
os.environ.setdefault("SMTP_HOST", "localhost")
os.environ.setdefault("SMTP_PORT", "25")
os.environ.setdefault("OPENAI_API_KEY", "test-openai-api-key")
os.environ.setdefault("AI_MODEL", "openai:gpt-4o-mini")
os.environ.setdefault("AI_EMBEDDING_MODEL", "openai:text-embedding-3-small")
