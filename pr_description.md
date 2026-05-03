🎯 **What:** The vulnerability fixed was debug mode being enabled by default in the application configuration.

⚠️ **Risk:** If left unfixed, debug mode being enabled could accidentally expose sensitive information, source code details, or detailed error traces in a production environment, leading to potential exploitation or data leakage.

🛡️ **Solution:** The default value for `debug` in `app/core/config.py` was changed to `False`. A unit test was also added in `tests/test_config.py` to ensure this secure default persists.
