class Text:
    welcome = """
         ██████  ██████  ██    ██ ██████  ██   ██  ██████  ███    ██ 
        ██       ██   ██  ██  ██  ██   ██ ██   ██ ██    ██ ████   ██ 
        ██   ███ ██████    ████   ██████  ███████ ██    ██ ██ ██  ██ 
        ██    ██ ██   ██    ██    ██      ██   ██ ██    ██ ██  ██ ██ 
         ██████  ██   ██    ██    ██      ██   ██  ██████  ██   ████ 
             
        Welcome to OW Gryphon - your data and analytics toolkit!
        (press Ctrl+C at any time to quit)
        
    """
    about = """
    Gryphon is ...
    
    Any bugs please talk to Dan Wang (he is the guilty)

    """
    first_prompt_question = "What would you like to do?"

    init_display_option = "Start a new project"
    generate_display_option = "Load template code into an existing project"
    add_display_option = "Install Python libraries/packages"
    about_display_option = "About OW Gryphon"
    quit_display_option = "Exit"

    menu_separator = "------------------------------"
    back_to_previous_menu_option = "<< Go back to the previous menu"
    type_library_name_menu_option = ">> Type the library name manually"
    first_prompt_instruction = "(Use arrow keys to select your option and press Enter)"

    generate_prompt_template_question = "Please select the template code you would to load:"

    init_prompt_template_question = "Please select the template you would like to use:"
    init_prompt_location_question = "Please give your project folder a name:"

    add_prompt_categories_question = "Navigate the categories:"
    add_prompt_instruction = " "
    add_prompt_type_library = "Type the name of the python library you want to install:"

    about_prompt_links = "Useful links:"

    base_confirmation = "Confirm to proceed with the actions from above?"

    # {arguments} is going to be replaced with the extra parameters from the template
    # {template_name} is going to be replaced with the template name
    generate_confirm_1 = "Confirm that you want to render the \"{template_name}\" template inside the current project."
    generate_confirm_2 = "\nUsing the following arguments: {arguments}"

    # {library_name} is going to be replaced with the library name
    add_confirm = "Confirm that you want to install the \"{library_name}\" library to the current project."

    # {location} is going to be replaced with the destination path
    # {template_name} is going to be replaced with the template name
    # {arguments} is going to be replaced with the extra parameters from the template
    init_confirm_1 = "\n\nConfirm that you want to start a new \"{template_name}\" project" \
                     "\nInside the folder \"{location}\""
    init_confirm_2 = "\nUsing the following arguments: {arguments}"

    generate_ask_extra_parameters = "Please fill some extra parameters needed for the template:"
