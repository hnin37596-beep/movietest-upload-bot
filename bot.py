import os
import boto3
from botocore.config import Config


# =========================================================
# ENVIRONMENT VARIABLES
# =========================================================

BOT_TOKEN = os.getenv("BOT_TOKEN")

R2_ACCOUNT_ID = os.getenv("R2_ACCOUNT_ID")
R2_ACCESS_KEY_ID = os.getenv("R2_ACCESS_KEY_ID")
R2_SECRET_ACCESS_KEY = os.getenv("R2_SECRET_ACCESS_KEY")
R2_BUCKET_NAME = os.getenv("R2_BUCKET_NAME", "movie-temp")


# =========================================================
# CHECK REQUIRED VARIABLES
# =========================================================

required = {
    "BOT_TOKEN": BOT_TOKEN,
    "R2_ACCOUNT_ID": R2_ACCOUNT_ID,
    "R2_ACCESS_KEY_ID": R2_ACCESS_KEY_ID,
    "R2_SECRET_ACCESS_KEY": R2_SECRET_ACCESS_KEY,
    "R2_BUCKET_NAME": R2_BUCKET_NAME,
}

missing = [name for name, value in required.items() if not value]

if missing:
    raise RuntimeError(
        "Missing required environment variables: "
        + ", ".join(missing)
    )


# =========================================================
# CLOUDFLARE R2
# =========================================================

R2_ENDPOINT = (
    f"https://{R2_ACCOUNT_ID}.r2.cloudflarestorage.com"
)

r2 = boto3.client(
    "s3",
    endpoint_url=R2_ENDPOINT,
    aws_access_key_id=R2_ACCESS_KEY_ID,
    aws_secret_access_key=R2_SECRET_ACCESS_KEY,
    region_name="auto",
    config=Config(
        signature_version="s3v4",
        retries={
            "max_attempts": 5,
            "mode": "adaptive",
        },
    ),
)


# =========================================================
# TEST R2 CONNECTION
# =========================================================

def test_r2():
    print("========================================")
    print("Cloudflare R2 Connection Test")
    print("========================================")
    print(f"Bucket: {R2_BUCKET_NAME}")
    print(f"Endpoint: {R2_ENDPOINT}")

    response = r2.list_objects_v2(
        Bucket=R2_BUCKET_NAME,
        MaxKeys=10,
    )

    objects = response.get("Contents", [])

    print(f"Objects found: {len(objects)}")

    for obj in objects:
        print(
            f" - {obj['Key']} "
            f"({obj['Size']} bytes)"
        )

    print("========================================")
    print("R2 CONNECTION OK")
    print("========================================")


# =========================================================
# MAIN
# =========================================================

if __name__ == "__main__":
    test_r2()
