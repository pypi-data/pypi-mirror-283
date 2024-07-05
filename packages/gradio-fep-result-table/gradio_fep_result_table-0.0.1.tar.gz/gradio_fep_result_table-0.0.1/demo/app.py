
import gradio as gr
from gradio_fep_result_table import fep_result_table

with gr.Blocks() as demo:
    with gr.Row():
        test = fep_result_table(placeholder='')
    def a(b):
        print(b)
    test.change(a, inputs=test)
if __name__ == "__main__":
    demo.launch()
