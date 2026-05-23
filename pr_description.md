🔒 Fix hardcoded CORS allowed origins

🎯 **What:** The vulnerability fixed
The CORS allowed_origins setting was hardcoded to only allow localhost ports 3000 and 8000, which made it impossible to configure the allowed CORS origins securely via environment variables for production deployments.

⚠️ **Risk:** The potential impact if left unfixed
If left unfixed, deploying this application to a production environment would require either maintaining a fork of the codebase or running with overly permissive or incorrectly configured CORS. If an administrator is forced to fork or manually patch the code to enable a frontend domain, they might inadvertently leave it open to Cross-Origin Resource Sharing (CORS) attacks if misconfigured.

🛡️ **Solution:** How the fix addresses the vulnerability
Updated the `allowed_origins` in `app/core/config.py` to allow specifying the list of allowed origins via the `ALLOWED_ORIGINS` environment variable. A `field_validator` parses a comma-separated string, making it easy to deploy the app with correct CORS settings through an environment variable.
