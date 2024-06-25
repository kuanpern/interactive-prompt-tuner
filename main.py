import os
import gradio as gr

# from components.TunerUI import tuner_block
from components.Chatbot import chatbot_block
from models import get_all_models

from dotenv import load_dotenv
load_dotenv()

max_historical_prompts = 10

# Variable declaration
model = get_all_models()[0]
states = gr.State()
chatbot = gr.Chatbot(elem_id="chatbot")


def variable_outputs(k):
    try:
        k = int(k)
    except:
        k = 1
    # end try
    return [gr.Textbox(visible=True)]*k + [gr.Textbox(visible=False)]*(max_historical_prompts-k)
# end def

def activate_chat_buttons():
    regenerate_btn = gr.Button(
        value="🔄  Regenerate", interactive=True, elem_id="regenerate_btn"
    )
    clear_btn = gr.ClearButton(
        elem_id="clear_btn",
        interactive=True,
    )
    return regenerate_btn, clear_btn


def deactivate_chat_buttons():
    regenerate_btn = gr.Button(
        value="🔄  Regenerate", interactive=False, elem_id="regenerate_btn"
    )
    clear_btn = gr.ClearButton(
        elem_id="clear_btn",
        interactive=False,
    )
    return regenerate_btn, clear_btn


def handle_message(
    user_input, temperature, top_p, max_output_tokens, states,
):
    history = states.value if states else []
    for hist in history:
        hist.append((user_input, None))
    for (
        updated_history,
        updated_states,
    ) in process_responses(
        temperature, top_p, max_output_tokens, history, states
    ):
        yield updated_history, updated_states


def regenerate_message(temperature, top_p, max_output_tokens, states, ):
    history = states.value if states else []
    user_input = (
        history.pop()[0] if history else None
    )  # Assumes regeneration is needed so there is at least one input
    for hist in history:
        hist.append((user_input, None))
    for (
        updated_history,        
        updated_states,
    ) in process_responses(
        temperature, top_p, max_output_tokens, history, states
    ):
        yield updated_history, updated_states


def process_responses(temperature, top_p, max_output_tokens, history, states):
    
    i = 0
    while True:
        i += 1
        if i > 10:
            break
        responses = str(i)+' .. '
        history[-1] = (history[-1][0], "".join(responses))
        states = gr.State(history)
        yield history, states

custom_css = """
css=".gradio-container {margin: 0px;} !important;"
"""
with gr.Blocks(
    css=custom_css,
    theme=gr.themes.Soft(secondary_hue=gr.themes.colors.sky),
) as demo:

    gr.Markdown(
        "# Interactive Prompt Tuner\n\nUse examples and AI assistant to tune instruction. "
    )

    with gr.Tab("Tuner"):
        with gr.Group(elem_id="input-group"):
            with gr.Accordion(f"Objectives", open=False):
                input_objective = gr.Textbox(
                    show_label=False,
                    placeholder="Optional objective to guide the model",
                    elem_id="input_objective",
                )


            with gr.Accordion(f"Input context", open=False):
                input_context = gr.Textbox(
                    show_label=False,
                    placeholder="Input article text",
                    elem_id="input_context",
                )


            with gr.Accordion("Prompt", open=True):
                with gr.Row():
                    cur_prompt_textbox = gr.Textbox(
                        label="Current prompt",
                        show_copy_button=True,
                        elem_id="cur_prompt_textbox",
                    )
                    prev_prompt_textbox = gr.Textbox(
                        label="Previous prompt",
                        show_copy_button=True,
                        elem_id="prev_prompt_textbox",
                        interactive=False
                    )
                # end with
            # end with

            with gr.Accordion("Response", open=True):
                with gr.Row() as result_row:
                    cur_result_textbox = gr.Textbox(
                        label="Current result",
                        elem_id="cur_result_textbox",
                    )
                    prev_result_textbox = gr.Textbox(
                        label="Previous result",
                        elem_id="prev_result_textbox",
                        interactive=False
                    )
                # end with
            # end with


        with gr.Row() as button_row:
            generate_btn = gr.Button(
                value="Generate result",
                elem_id="generate_btn",
            )
            regenerate_btn = gr.Button(
                value="Suggest new prompt", elem_id="regenerate_btn"
            )
            revert_btn = gr.Button(
                value="Revert to previous prompt", elem_id="regenerate_btn"
            )

            clear_btn = gr.ClearButton(
                elem_id="clear_btn",
            )



        with gr.Row():
            examples = gr.Examples(
                [
                    "Can you tell me about the weather?",
                    "What is the capital of France?",
                    "What is the meaning of life?",
                ],
                inputs=[input_context],
                label="Example inputs",
            )

        with gr.Accordion("Parameters", open=False) as parameter_row:
            model = gr.Dropdown(
                ["gpt-3.5-turbo", "gpt-4"],
                value="gpt-3.5-turbo",
                label="Model",
            )


            temperature = gr.Slider(
                minimum=0.0,
                maximum=2.0,
                value=0.0,
                step=0.1,
                interactive=True,
                label="Temperature",
            )
            top_p = gr.Slider(
                minimum=0.0,
                maximum=1.0,
                value=1.0,
                step=0.1,
                interactive=True,
                label="Top P",
            )
            max_output_tokens = gr.Slider(
                minimum=16,
                maximum=4096,
                value=1024,
                step=64,
                interactive=True,
                label="Max output tokens",
            )


        generate_btn.click(
            handle_message,
            inputs=[
                input_context,
                temperature,
                top_p,
                max_output_tokens,
                states,
                
            ],
            outputs=[chatbot, states, ],
        ).then(
            activate_chat_buttons,
            inputs=[],
            outputs=[regenerate_btn, clear_btn],
        )

        regenerate_btn.click(
            regenerate_message,
            inputs=[
                temperature,
                top_p,
                max_output_tokens,
                states,
                
            ],
            outputs=[chatbot, states, ],
        )

        clear_btn.click(
            deactivate_chat_buttons,
            inputs=[],
            outputs=[regenerate_btn, clear_btn],
        ).then(inputs=None, outputs=[model])
    # end with

    with gr.Tab("Chatbot"):
        chatbot_block.render()
    # end with

    with gr.Tab("Prompt History"):
        s = gr.Slider(1, max_historical_prompts, value=max_historical_prompts, step=1, label="How many historical_prompts to show:")
        historical_prompts = []
        for i in range(max_historical_prompts):
            t = gr.Textbox(f"History {i}", show_copy_button=True, interactive=False)
            historical_prompts.append(t)

        s.change(variable_outputs, s, historical_prompts)

    # end with


# end with


if __name__ == "__main__":
    if os.getenv('PROXY_PATH_PREFIX') is not None:
        root_path = os.getenv('PROXY_PATH_PREFIX')+'/app_pool/interactive-prompt-tuner'
    else:
        root_path = None
    # end if

    demo.queue(max_size=100).launch(
        server_port = int(os.getenv('SERVER_PORT', 8080)),
        root_path=root_path,
    ) # end launch
# end if
