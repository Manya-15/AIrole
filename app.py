import os
import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO

def split_name(name):
    words = name.split()
    if len(words) == 1:
        return name, ""
    elif len(words) == 2:
        return words[0], words[1]
    elif len(words) == 3:
        return " ".join(words[:2]), words[2]
    else:
        return " ".join(words[:2]), " ".join(words[2:])


def showTemplateTwo():
    # Load the image
    img = Image.open(template_path)
    # Submit button
    
    if user_name:
        # Split name into first name and surname
        first_name, surname = split_name(user_name)

        # Create a copy of the image to draw on
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)

        # Draw the first name
        font_size = max_font_size
        while True:
            font = ImageFont.truetype(font_path, font_size)
            # Use textbbox to get the width and height of the first name text
            text_bbox = draw.textbbox((0, 0), first_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Check if text fits within the first name box
            if text_width <= first_name_box_width and text_height <= first_name_box_height:
                break
            font_size -= 1

        # Calculate position to center the first name within the box
        first_name_x = first_name_box_x + (first_name_box_width - text_width) // 2
        first_name_y = first_name_box_y + (first_name_box_height - text_height) // 2

        # Draw the first name on the image
        draw.text((first_name_x, first_name_y), first_name, font=font, fill="white")

        # Draw the surname if present
        if surname:
            font_size = max_font_size
            while True:
                font = ImageFont.truetype(font_path, font_size)
                # Use textbbox to get the width and height of the surname text
                text_bbox = draw.textbbox((0, 0), surname, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]
                
                # Check if text fits within the surname box
                if text_width <= surname_box_width and text_height <= surname_box_height:
                    break
                font_size -= 1

            # Calculate position to center the surname within the box
            surname_x = surname_box_x + (surname_box_width - text_width) // 2
            surname_y = surname_box_y + (surname_box_height - text_height) // 2

            # Draw the surname on the image in the specified color
            draw.text((surname_x, surname_y), surname, font=font, fill=surname_color)

        # Display the modified image
        st.image(img_copy, caption="Your Personalized Template", use_column_width=True)

        # Save modified image to an in-memory buffer for download
        buffer = BytesIO()
        img_copy.save(buffer, format="PNG")
        buffer.seek(0)

        # Provide a download button
        st.download_button(
            label="Download Your Image",
            data=buffer,
            file_name=f"{user_name}_{assigned_role}.png",
            mime="image/png"
        )
    else:
        st.warning("Please enter your name.")

def showTemplateOne():
    # Load the image
    img = Image.open(template_path)
    if user_name:
        # Create a copy of the image to draw on
        img_copy = img.copy()
        draw = ImageDraw.Draw(img_copy)

        # Find the maximum font size that fits within the text box
        font_size = max_font_size
        while True:
            font = ImageFont.truetype(font_path, font_size)
            # Use textbbox to get the width and height of the text
            text_bbox = draw.textbbox((0, 0), user_name, font=font)
            text_width = text_bbox[2] - text_bbox[0]
            text_height = text_bbox[3] - text_bbox[1]
            
            # Check if text fits within the box
            if text_width <= text_box_width and text_height <= text_box_height:
                break
            # Decrease the font size if text is too big
            font_size -= 1

        # Calculate position to center the text within the box
        text_x = text_box_x + (text_box_width - text_width) // 2
        text_y = text_box_y + (text_box_height - text_height) // 2

        # Draw the text on the image
        draw.text((text_x, text_y), user_name, font=font, fill="white")

        # Display the modified image
        st.image(img_copy, caption="Your Personalized Template", use_column_width=True)

        # Save modified image to an in-memory buffer for download
        buffer = BytesIO()
        img_copy.save(buffer, format="PNG")
        buffer.seek(0)

        # Provide a download button
        st.download_button(
            label="Download Your Image",
            data=buffer,
            file_name=f"{user_name}_template.png",
            mime="image/png"
        )
    else:
        st.warning("Please enter your name.")

st.set_page_config(
    page_title="Future AI Role",
    page_icon="🤖",
    layout="wide"
)


# Directory path for role templates
template_dir = "role_templates"  # Ensure the directory exists and contains the necessary folders and templates

# Title and description
st.title("Discover Your AI Role!")
st.write("""
Take this quiz to find out your unique AI role and how you can contribute to the field of AI for sustainability, regardless of your technical background!
""")
# Creating sidebar
with st.sidebar:
    st.header("Share your Role")
    st.write("     ")
    st.write("Share your personalized template on Instagram or your story and tag us @sdgyouthleaders and @1m1b_ipu to get featured!")



# Add form for quiz questions
with st.form("quiz_form"):
    # User information
    user_name = st.text_input("What is your name?")
    gender = st.radio("Your gender?", ["male", "female"])

    # Questions
    q1 = st.radio("What motivates you the most?", ["Making a positive impact", "Exploring new ideas", "Solving complex problems", "Connecting with people", "Creating innovative solutions"])
    q2 = st.radio("How do you prefer to work on a problem?", ["Researching and analyzing data", "Brainstorming creative solutions", "Breaking down tasks step-by-step", "Collaborating with others", "Focusing on big-picture ideas"])
    q3 = st.radio("Which skill describes you best?", ["Attention to detail", "Creativity", "Problem-solving", "Communication", "Visionary thinking"])
    q4 = st.radio("How comfortable are you with technology?", ["Very comfortable", "Moderately comfortable", "A little comfortable", "Not comfortable at all"])
    q5 = st.radio("What is your favorite way to learn about new topics?", ["Reading articles or research papers", "Watching videos or tutorials", "Experimenting hands-on", "Discussing with others"])

    # Submit button
    submitted = st.form_submit_button("Submit")

# Role descriptions and assignments
roles = {
    "The Creative Innovator": ["Exploring new ideas", "Brainstorming creative solutions", "Creativity"],
    "The Ethical Advisor": ["Making a positive impact", "Collaborating with others", "Communication"],
    "The Data Detective": ["Solving complex problems", "Researching and analyzing data", "Attention to detail"],
    "The Tech Visionary": ["Creating innovative solutions", "Focusing on big-picture ideas", "Visionary thinking"],
    "The Communicator": ["Connecting with people", "Collaborating with others", "Communication"],
    "The Sustainability Strategist": ["Making a positive impact", "Breaking down tasks step-by-step", "Problem-solving"],
    "The Educator": ["Connecting with people", "Discussing with others", "Communication"],
    "The Problem Solver": ["Solving complex problems", "Experimenting hands-on", "Problem-solving"]
}

role_descriptions = {
    "The Creative Innovator": "You love brainstorming and generating fresh ideas. As a Creative Innovator, you can help design AI solutions for sustainable urban planning, renewable energy, and climate action.",
    "The Ethical Advisor": "You prioritize ethical considerations and impact. As an Ethical Advisor, you can ensure AI solutions respect privacy, fairness, and social good, vital for sustainable development.",
    "The Data Detective": "With your attention to detail, you excel at analyzing patterns. As a Data Detective, you can work on projects like climate modeling, tracking biodiversity, or optimizing resource use.",
    "The Tech Visionary": "You think big and focus on the future. As a Tech Visionary, you can drive initiatives that use AI to predict and mitigate environmental issues, like deforestation or water scarcity.",
    "The Communicator": "You are skilled at explaining complex ideas. As a Communicator, you can educate the public on sustainable AI practices and advocate for climate-friendly AI applications.",
    "The Sustainability Strategist": "You have a knack for structured planning. As a Sustainability Strategist, you can design AI projects aimed at reducing waste, conserving resources, or promoting renewable energy.",
    "The Educator": "You love sharing knowledge. As an Educator, you can help raise awareness about AI's role in sustainability and inspire others to support AI for good.",
    "The Problem Solver": "You enjoy tackling tough challenges. As a Problem Solver, you can work on AI projects addressing global issues, like reducing carbon emissions or improving agricultural efficiency."
}

# Only process the answers and display the result if the form is submitted
if submitted:
    # Role assignment logic based on answers
    role_count = {role: 0 for role in roles}
    answers = [q1, q2, q3, q4, q5]

    for answer in answers:
        for role, keywords in roles.items():
            if answer in keywords:
                role_count[role] += 1

    # Select the role with the highest count
    assigned_role = max(role_count, key=role_count.get)

    # Display the result
    st.subheader(f"Your AI Role: {assigned_role}")
    st.write(f"Here's how you, as a **{assigned_role}**, can contribute to AI and sustainability:")
    st.write(role_descriptions[assigned_role])
    st.write("Download the below made template and share your personalized template on Instagram or your story and tag us @sdgyouthleaders and @1m1b_ipu to get featured!")


    # Search for the template based on the role and gender
    role_folder = os.path.join(template_dir, assigned_role)
    template_path = os.path.join(role_folder, f"{gender}.png")

    if assigned_role == "The Creative Innovator":
        font_path = "SK Cuber.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 26.3  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 315.7  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 435.3  # Width of the first name text box
        first_name_box_height = 82.9  # Height of the first name text box
        max_font_size = 60  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 26.3  # Set your own x-coordinate for surname box
        surname_box_y = 398.6  # Set your own y-coordinate for surname box
        surname_box_width = 466  # Width of the surname text box
        surname_box_height = 82.9  # Height of the surname text box
        surname_color = "#ea8d20"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Ethical Advisor":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties
        text_box_x = 108  # x-coordinate of the top-left corner of the text box
        text_box_y = 691.8  # y-coordinate of the top-left corner of the text box
        text_box_width = 863.7  # Width of the text box
        text_box_height = 85.6  # Height of the text box
        max_font_size = 60  # Maximum font size to start with
        showTemplateOne()

    elif assigned_role == "The Data Detective":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 506.6  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 767  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 487.6  # Width of the first name text box
        first_name_box_height = 82.9  # Height of the first name text box
        max_font_size = 60  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 513.4  # Set your own x-coordinate for surname box
        surname_box_y = 868.4  # Set your own y-coordinate for surname box
        surname_box_width = 487.6  # Width of the surname text box
        surname_box_height = 82.9  # Height of the surname text box
        surname_color = "#dbff3d"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Tech Visionary":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 65.7  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 495.5  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 580.5  # Width of the first name text box
        first_name_box_height = 111.7  # Height of the first name text box
        max_font_size = 70  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 65.7  # Set your own x-coordinate for surname box
        surname_box_y = 575.2  # Set your own y-coordinate for surname box
        surname_box_width = 580.5  # Width of the surname text box
        surname_box_height = 111.7  # Height of the surname text box
        surname_color = "#c40e84"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Communicator":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 33  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 540  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 601.9  # Width of the first name text box
        first_name_box_height = 114.2  # Height of the first name text box
        max_font_size = 60  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 33  # Set your own x-coordinate for surname box
        surname_box_y = 617.5  # Set your own y-coordinate for surname box
        surname_box_width = 601.9  # Width of the surname text box
        surname_box_height = 103.3  # Height of the surname text box
        surname_color = "#ff7b01"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Sustainability Strategist":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 33.9  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 525.2 # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 568.6  # Width of the first name text box
        first_name_box_height = 111.7  # Height of the first name text box
        max_font_size = 70  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 33.9  # Set your own x-coordinate for surname box
        surname_box_y = 605.3  # Set your own y-coordinate for surname box
        surname_box_width = 568.6  # Width of the surname text box
        surname_box_height = 107.5  # Height of the surname text box
        surname_color = "#fff4ec"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Educator":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 39.2  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 491.9  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 498.3  # Width of the first name text box
        first_name_box_height = 114.2  # Height of the first name text box
        max_font_size = 60  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 39.2  # Set your own x-coordinate for surname box
        surname_box_y = 573.2  # Set your own y-coordinate for surname box
        surname_box_width = 498.3  # Width of the surname text box
        surname_box_height = 103.3  # Height of the surname text box
        surname_color = "#ff7b01"  # Color for the surname text
        showTemplateTwo()

    elif assigned_role == "The Problem Solver":
        font_path = "lastica.ttf"  # Adjust the path to your SK Cuber font
        # Text box properties for first name
        first_name_box_x = 55.3  # x-coordinate of the top-left corner of the first name text box
        first_name_box_y = 446.5  # y-coordinate of the top-left corner of the first name text box
        first_name_box_width = 584.8  # Width of the first name text box
        first_name_box_height = 111.7  # Height of the first name text box
        max_font_size = 60  # Maximum font size to start with

        # Text box properties for surname
        surname_box_x = 55.3  # Set your own x-coordinate for surname box
        surname_box_y = 531  # Set your own y-coordinate for surname box
        surname_box_width = 584.8  # Width of the surname text box
        surname_box_height = 111.7  # Height of the surname text box
        surname_color = "#ff7b01"  # Color for the surname text
        showTemplateTwo()
        
    else:
        st.warning("No role assigned")
    
                

