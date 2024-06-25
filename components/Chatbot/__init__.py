import gradio as gr

# from langchain_core.prompts import PromptTemplate
# from langchain_core.output_parsers import StrOutputParser
# from langchain_google_genai import ChatGoogleGenerativeAI


def alternatingly_agree(message, history):
    if len(history) % 2 == 0:
        return f"Yes, I do think that '{message}'"
    else:
        return "I don't think so"
    # end if
# end def


with gr.Blocks(
    title="General chatbot",
) as chatbot_block:
    gr.ChatInterface(alternatingly_agree)
# end with
