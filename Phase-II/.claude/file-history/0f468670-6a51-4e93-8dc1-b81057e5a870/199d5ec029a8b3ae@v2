from backend.config.settings import settings
print("DATABASE_URL from settings:", repr(settings.DATABASE_URL))

# Test the conversion logic
if settings.DATABASE_URL.startswith("sqlite"):
    db_url = settings.DATABASE_URL.replace("sqlite:///", "sqlite+aiosqlite:///")
else:
    db_url = settings.DATABASE_URL

print("Converted db_url:", repr(db_url))