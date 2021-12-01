# %%

from IPython.display import HTML, Javascript, display



# %%
#IPython.display.HTML("<div><h1>THIS IS A TITLE</h1><p>And this is a paragraph; and if all this works it's freakin' awesome</p></div>")
# %% using HTML, js works erratically (usually: yes on first execution of cell, not afterwards...)

HTML("""
<div>
    <h1>THIS IS A TITLE</h1>
    <p>And this is a paragraph; and if all this works it's freakin' awesome</p>
    <p id='i-want-to-be-free'>And this paragraph wants to be filled up by javascript</p>
    <script>
        let my_paragraph = document.getElementById("i-want-to-be-free")
        my_paragraph.innerHTML = "I WANT TO BE FREEEEEE! ...But js only works occasionally from an IPython.display.HTML() call..."
    </script>
</div>
""")
# %% using HTML & classname

HTML("""
<div>
    <h1>THIS IS A TITLE</h1>
    <p>And this is a paragraph; and if all this works it's freakin' awesome</p>
    <p class='classyy'>And this paragraph wants to be filled up by javascript</p>
    <script>
        let my_paragraphs = document.getElementsByClassName("classyy")
        my_paragraphs.forEach(p=>{
            p.innerHTML = "Classy baby."
        })
    </script>
</div>
""")

# %%

display(Javascript("""
element.append("APPENDING TEXT TO ELEMENT")
"""))
# %%

display(Javascript("""
element.append("<h1 id='title'>THIS IS A TITLE that was added thanks to JS</h1><p>And this paragraph too</p>")
"""))
# %%


display(Javascript("""
element.append("<h1 id='title'>THIS IS A TITLE that was added thanks to JS</h1><p>And this paragraph too</p>")
let my_title = document.getElementById("i-want-to-be-free")
my_title.addEventListener("mouseover", e=> {
  my_title.setAttribute("style", "background-color:blue;")  
})
my_title.addEventListener("mouseout", e=> {
  my_title.setAttribute("style", "background-color:white;")  
})
"""))

# %% javascript

display(Javascript("""
let my_paragraph = document.getElementById("i-want-to-be-free")
my_paragraph.innerHTML = "I'm doing fucked up shit in VS code interactive window MUHAHAHAHAHA!!!'"
"""))

# %%


display(Javascript("""
IPython.notebook.kernel.execute('Alfred_life="huhu";');
"""))


# %%

from IPython.display import HTML, Javascript, display

display(HTML("""
<p id="demo">A Paragraph.</p>
<button id="something">Try it</button>
"""))
js = """
$(document).ready(
function() {
    $("#something").click(function() {
        $('#demo').text("Changed text");
        $('#something').text('Change button');
        });
    });
"""
js = Javascript(js)
display(js)
# %%
