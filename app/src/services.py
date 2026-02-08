from baml_client import b
from baml_client.types import (
    Theme,
    ClassificationOutput,
    FormOutput,
    ProbabilisticClassificationOutput,
)
import asyncio
from collections import Counter
import json
import re
from langfuse import observe, get_client
from dotenv import load_dotenv

load_dotenv()


langfuse = get_client()

# Verify connection
if langfuse.auth_check():
    print("✅ Langfuse client is authenticated and ready!")
else:
    print("❌ Authentication failed. Please check your credentials and host.")


class DataExtractionService:
    # Text classification
    @staticmethod
    @observe(name="classify-text")
    async def classify_text(text: str, themes: list[Theme]) -> ClassificationOutput:
        langfuse.update_current_trace(user_id=1, tags=["testing", "/classify"])
        res = await b.ClassifyText(text=text, themes=themes)
        return res

    # Form completion
    @staticmethod
    @observe(name="complete_form")
    async def complete_form(text: str) -> FormOutput:
        langfuse.update_current_trace(user_id=1, tags=["testing", "/complete-form"])
        return await b.ExtractForm(text=text)

    # Probabilistic clasification
    @staticmethod
    @observe(name="classify_probabilistic")
    async def classify_probabilistic(
        text: str, themes: list[Theme], nbr_iter: int = 5
    ) -> ProbabilisticClassificationOutput:
        langfuse.update_current_trace(
            user_id=1, tags=["testing", "/classify-probabilistic"]
        )
        tasks = [b.ClassifyText(text=text, themes=themes) for _ in range(nbr_iter)]
        results = await asyncio.gather(*tasks)
        ## Get most common title from results
        theme_counts = Counter([res.chosen_theme.title for res in results])
        most_common_title, count = theme_counts.most_common(1)[0]
        ## Calculate confidence
        confidence = count / nbr_iter
        winner_theme = next(
            res.chosen_theme
            for res in results
            if res.chosen_theme.title == most_common_title
        )
        ##

        return ProbabilisticClassificationOutput(
            chosen_theme=winner_theme, confidence=confidence
        )

    # Probabilistic clasification approach 2
    @staticmethod
    @observe(name="classify_probabilistic_2")
    async def classify_probabilistic_2(
        text: str, themes: list[Theme]
    ) -> ProbabilisticClassificationOutput:
        langfuse.update_current_trace(
            user_id=1, tags=["testing", "/classify-probabilistic-2"]
        )
        my_clients = ["Haiku", "Sonnet", "Opus"]
        tasks = [
            b.ClassifyText(text=text, themes=themes, baml_options={"client": cl})
            for cl in my_clients
        ]
        results = await asyncio.gather(*tasks)
        ## Get most common title from results
        theme_counts = Counter([res.chosen_theme.title for res in results])
        most_common_title, count = theme_counts.most_common(1)[0]
        ## Calculate confidence
        confidence = count / len(my_clients)
        winner_theme = next(
            res.chosen_theme
            for res in results
            if res.chosen_theme.title == most_common_title
        )
        ##

        return ProbabilisticClassificationOutput(
            chosen_theme=winner_theme, confidence=confidence
        )

    # Streaming the response
    @staticmethod
    @observe(name="stream_complete_form")
    async def stream_complete_form(text: str):
        langfuse.update_current_trace(
            user_id=1, tags=["testing", "/complete-form-stream"]
        )
        stream = b.stream.ExtractForm(text=text)

        async for partial_form in stream:
            if partial_form:
                yield partial_form.model_dump_json() + "\n"

    # dynamic extraction
    @staticmethod
    @observe(name="extract_generalized")
    async def extract_generalized(text: str, schema_description: dict) -> dict:
        langfuse.update_current_trace(
            user_id=1, tags=["testing", "/extract-generalized"]
        )
        raw_response = await b.ExtractDynamicForm(
            text=text, schema_description=json.dumps(schema_description, indent=2)
        )

        # Cleaning
        clean_json = raw_response
        match = re.search(r"(\{.*\})", raw_response, re.DOTALL)
        if match:
            clean_json = match.group(1)
        else:
            # Si on ne trouve pas de { }, on essaie de virer les backticks au cas où
            clean_json = raw_response.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(clean_json)

        except json.JSONDecodeError:
            return {"error": "Failed to parse LLM response as JSON", "raw": clean_json}


extraction_service = DataExtractionService()
