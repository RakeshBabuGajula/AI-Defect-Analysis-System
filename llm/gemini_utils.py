import time


def generate_content_with_retry(
    model,
    prompt,
    retries=4,
    initial_delay=20
):
    """
    Generate content using Gemini model with automatic exponential backoff 
    when encountering 429 Rate Limit / ResourceExhausted errors.
    """
    delay = initial_delay

    for attempt in range(retries):
        try:
            return model.generate_content(prompt)
        except Exception as e:
            err_msg = str(e).lower()
            if (
                "429" in err_msg
                or "quota" in err_msg
                or "resourceexhausted" in err_msg
                or "rate limit" in err_msg
            ) and attempt < retries - 1:
                sleep_time = delay
                if "retry in " in err_msg:
                    try:
                        part = err_msg.split("retry in ")[1].split("s")[0]
                        extracted_s = float(part)
                        if extracted_s > 0:
                            sleep_time = max(sleep_time, int(extracted_s) + 3)
                    except Exception:
                        pass

                print(
                    f"[Gemini 429 Quota Exceeded] Retrying in {sleep_time}s... "
                    f"(Attempt {attempt + 1}/{retries})"
                )
                time.sleep(sleep_time)
                delay *= 2
            else:
                raise e
