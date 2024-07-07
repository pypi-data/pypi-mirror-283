
import gradio as gr
from app import demo as app
import os

_docs = {'ImagePrompter': {'description': 'Create an image prompter to upload images and process point/box prompts.', 'members': {'__init__': {'value': {'type': 'str | _Image.Image | np.ndarray | None', 'default': 'None', 'description': 'A PIL Image, numpy array, path or URL for the default value. If callable, it will be called set the initial value.'}, 'height': {'type': 'int | None', 'default': 'None', 'description': 'Height of the displayed image in pixels.'}, 'width': {'type': 'int | None', 'default': 'None', 'description': 'Width of the displayed image in pixels.'}, 'image_mode': {'type': 'Literal[\n    "1",\n    "L",\n    "P",\n    "RGB",\n    "RGBA",\n    "CMYK",\n    "YCbCr",\n    "LAB",\n    "HSV",\n    "I",\n    "F",\n]', 'default': '"RGB"', 'description': '"RGB" if color, or "L" if black and white. See https://pillow.readthedocs.io/en/stable/handbook/concepts.html.'}, 'sources': {'type': 'list[Literal["upload", "clipboard"]] | None', 'default': 'None', 'description': 'List of sources for the image.'}, 'type': {'type': 'Literal["numpy", "pil", "filepath"]', 'default': '"numpy"', 'description': 'The format the image is converted before being passed into the prediction function.'}, 'label': {'type': 'str | None', 'default': 'None', 'description': 'The label for this component.'}, 'every': {'type': 'float | None', 'default': 'None', 'description': "If `value` is a callable, run the function 'every' number of seconds while the client connection is open."}, 'show_label': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will display label.'}, 'show_download_button': {'type': 'bool', 'default': 'True', 'description': 'If True, will display button to download image.'}, 'container': {'type': 'bool', 'default': 'True', 'description': 'If True, will place the component in a container - providing some extra padding around the border.'}, 'scale': {'type': 'int | None', 'default': 'None', 'description': 'relative width compared to adjacent Components in a Row. Should be an integer.'}, 'min_width': {'type': 'int', 'default': '160', 'description': 'minimum pixel width, will wrap if not sufficient screen space to satisfy this value.'}, 'interactive': {'type': 'bool | None', 'default': 'None', 'description': 'if True, will allow users to upload and edit an image; if False, can only be used to display images.'}, 'visible': {'type': 'bool', 'default': 'True', 'description': 'If False, component will be hidden.'}, 'elem_id': {'type': 'str | None', 'default': 'None', 'description': 'An optional string that is assigned as the id of this component in the HTML DOM.'}, 'elem_classes': {'type': 'list[str] | str | None', 'default': 'None', 'description': 'An optional list of strings that are assigned as the classes of this component in the HTML DOM.'}, 'render': {'type': 'bool', 'default': 'True', 'description': 'If False, component will not render be rendered in the Blocks context.'}, 'show_share_button': {'type': 'bool | None', 'default': 'None', 'description': 'If True, show a share icon that allows user to share outputs to Hugging Face Spaces Discussions.'}}, 'postprocess': {'y': {'type': 'PromptValue', 'description': None}, 'value': {'type': 'PromptValue', 'description': None}}, 'preprocess': {'return': {'type': 'PromptValue | None', 'description': 'Passes the uploaded image as a `numpy.array`, `PIL.Image` or `str` filepath depending on `type`. For SVGs, the `type` parameter is ignored and the filepath of the SVG is returned.'}, 'value': None}}, 'events': {'clear': {'type': None, 'default': None, 'description': 'This listener is triggered when the user clears the ImagePrompter using the X button for the component.'}, 'change': {'type': None, 'default': None, 'description': 'Triggered when the value of the ImagePrompter changes either because of user input (e.g. a user types in a textbox) OR because of a function update (e.g. an image receives a value from the output of an event trigger). See `.input()` for a listener that is only triggered by user input.'}, 'stream': {'type': None, 'default': None, 'description': 'This listener is triggered when the user streams the ImagePrompter.'}, 'select': {'type': None, 'default': None, 'description': 'Event listener for when the user selects or deselects the ImagePrompter. Uses event data gradio.SelectData to carry `value` referring to the label of the ImagePrompter, and `selected` to refer to state of the ImagePrompter. See EventData documentation on how to use this event data'}, 'upload': {'type': None, 'default': None, 'description': 'This listener is triggered when the user uploads a file into the ImagePrompter.'}}}, '__meta__': {'additional_interfaces': {}, 'user_fn_refs': {'ImagePrompter': []}}}

abs_path = os.path.join(os.path.dirname(__file__), "css.css")

with gr.Blocks(
    css=abs_path,
    theme=gr.themes.Default(
        font_mono=[
            gr.themes.GoogleFont("Inconsolata"),
            "monospace",
        ],
    ),
) as demo:
    gr.Markdown(
"""
# `gradio_image_prompter_visible_box`

<div style="display: flex; gap: 7px;">
<img alt="Static Badge" src="https://img.shields.io/badge/version%20-%200.1.0%20-%20orange">  
</div>

A gradio component to upload images and process point/box prompts with more visible boxes.
""", elem_classes=["md-custom"], header_links=True)
    app.render()
    gr.Markdown(
"""
## Installation

```bash
pip install gradio_image_prompter_visible_box
```

## Usage

```python
import gradio as gr
from gradio_image_prompter import ImagePrompter

demo = gr.Interface(
    lambda prompts: (prompts["image"], prompts["points"]),
    ImagePrompter(show_label=False),
    [gr.Image(show_label=False), gr.Dataframe(label="Points")],
)
if __name__ == '__main__':
    demo.launch()

```
""", elem_classes=["md-custom"], header_links=True)


    gr.Markdown("""
## `ImagePrompter`

### Initialization
""", elem_classes=["md-custom"], header_links=True)

    gr.ParamViewer(value=_docs["ImagePrompter"]["members"]["__init__"], linkify=[])


    gr.Markdown("### Events")
    gr.ParamViewer(value=_docs["ImagePrompter"]["events"], linkify=['Event'])




    gr.Markdown("""

### User function

The impact on the users predict function varies depending on whether the component is used as an input or output for an event (or both).

- When used as an Input, the component only impacts the input signature of the user function.
- When used as an output, the component only impacts the return signature of the user function.

The code snippet below is accurate in cases where the component is used as both an input and an output.

- **As input:** Is passed, passes the uploaded image as a `numpy.array`, `PIL.Image` or `str` filepath depending on `type`. For SVGs, the `type` parameter is ignored and the filepath of the SVG is returned.


 ```python
def predict(
    value: PromptValue | None
) -> PromptValue:
    return value
```
""", elem_classes=["md-custom", "ImagePrompter-user-fn"], header_links=True)




    demo.load(None, js=r"""function() {
    const refs = {};
    const user_fn_refs = {
          ImagePrompter: [], };
    requestAnimationFrame(() => {

        Object.entries(user_fn_refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}-user-fn`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })

        Object.entries(refs).forEach(([key, refs]) => {
            if (refs.length > 0) {
                const el = document.querySelector(`.${key}`);
                if (!el) return;
                refs.forEach(ref => {
                    el.innerHTML = el.innerHTML.replace(
                        new RegExp("\\b"+ref+"\\b", "g"),
                        `<a href="#h-${ref.toLowerCase()}">${ref}</a>`
                    );
                })
            }
        })
    })
}

""")

demo.launch()
