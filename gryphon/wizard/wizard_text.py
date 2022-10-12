class Text:
    welcome = """ 
            █████████                                 █████                         
           ███     ███                                 ███                          
          ███          ████████  █████ ████ ████████   ███████    ██████  ████████  
          ███           ███  ███  ███  ███   ███  ███  ███  ███  ███  ███  ███  ███ 
          ███    █████  ███       ███  ███   ███  ███  ███  ███  ███  ███  ███  ███ 
           ███    ███   ███       ███  ███   ███  ███  ███  ███  ███  ███  ███  ███ 
            █████████  █████       ███████   ███████  ████ █████  ██████  ████ █████
                                      ███   ███                                    
                                 ███  ███   ███                                    
                                  ██████   █████                         
        
        Welcome to OW Gryphon - your data and analytics toolkit!
        (press Ctrl+C at any time to quit)

    """
    about = """
    Gryphon is a toolkit designed to make it easy to use Python for data analytics. 
    With automatic project directory and environment creation, OW-style graphical 
    visualizations and numerous resources for different methodologies and use cases, 
    Gryphon is designed to be your one-stop-Python-shop! 
    
    Owners:
    - Daniel Wang (daniel.wang@oliverwyman.com)
    - Daniel Uken (daniel.uken@oliverwyman.com)
    
    Developers:
    - Vittor Pereira (vittor.pereira@oliverwyman.com)

    """

    first_prompt_question = "What would you like to do?"

    init_display_option = "Start a new Gryphon project"
    init_from_existing_display_option = "Set up Gryphon with an existing project folder"
    generate_display_option = "Load template code into an existing Gryphon project"
    add_display_option = "Install Python libraries/packages"
    handover_display_option = "Hand over project"
    about_display_option = "About OW Gryphon"
    settings_display_option = "Advanced options"
    feedback_display_option = "General contact/feedback"
    report_bug_display_option = "Report bug"
    contact_us_display_option = "Contact us (bugs, feedback, etc.)"
    configure_project_display_option = "Configure Gryphon project defaults and logs"
    quit_display_option = "Exit"

    menu_separator = "------------------------------"
    back_to_previous_menu_option = "<< Go back to the previous menu"
    type_library_name_menu_option = ">> Type the library name manually"
    first_prompt_instruction = "(Use arrow keys to select your option and press Enter)"

    generate_prompt_template_question = "Please select the template code you would to load:"

    init_prompt_template_question = "Please select the template you would like to use:"
    init_prompt_location_question = "Please give your project folder a name:"
    init_prompt_addons = "Select the extras that you would like to add to the project and then press Enter:"
    init_prompt_init_from_existing = "Did you mean to set up a Gryphon project from an existing folder instead?"

    init_from_existing_prompt_location_question = "Select the target folder (blank if current folder):"
    init_from_existing_confirm_conda_question = "An existing conda environment was found inside the project folder," \
                                                " do you want to use it as the project environment?"
    init_from_existing_confirm_venv_question = "An existing venv environment was found inside the project folder," \
                                               " do you want to use it as the project environment?"
    init_from_existing_point_to_external_env = "Do you want to point to an external environment?"
    init_from_existing_ask_external_env_path = "Type the external environment path:"

    add_prompt_categories_question = "Navigate the categories:"
    add_prompt_instruction = " "
    add_prompt_type_library = "Type the names of the python libraries you want to install (separated by spaces):"
    add_prompt_type_version = "Type the version you want to install:"

    handover_prompt_folder_question = "Type the project folder (blank if current folder):"
    handover_prompt_new_size_limit_question = "Type the new size limit you want to use in MBs, current limit: " \
                                              "{limit} MB (type a negative number to cancel and go back):"
    handover_prompt_include_large_files_question = "Some large files were found. Do you want to include them in " \
                                                   "the package:"
    handover_prompt_confirm_configurations = "Confirm that you want to proceed with the configurations from above. " \
                                             "The following file will be created: "
    handover_prompt_change_settings = "Select the setting you want to change:"
    handover_prompt_gryphon_files_policy = "Select what to do with Gryphon generated files:"
    handover_prompt_large_files_policy = "Select what to do with large files:"

    about_prompt_links = "Useful links:"

    base_confirmation = "Confirm to proceed with the actions from above?"

    # {arguments} is going to be replaced with the extra parameters from the template
    # {template_name} is going to be replaced with the template name
    generate_confirm_1 = "Confirm that you want to render the \"{template_name}\" template inside the current project."
    generate_confirm_2 = "\nUsing the following arguments: {arguments}"

    # {library_name} is going to be replaced with the library name
    add_confirm = "Confirm that you want to install the \"{library_name}\" library to the current project."
    add_confirm_multiple = "Confirm that you want to install the following libraries to the current project: " \
                           "{libraries}"

    # {location} is going to be replaced with the destination path
    # {template_name} is going to be replaced with the template name
    # {arguments} is going to be replaced with the extra parameters from the template
    init_confirm_1 = "Confirm that you want to start a new \"{template_name}\" project" \
                     "\ninside the folder \"{location}\""
    init_confirm_2 = "\nUsing the following arguments: {arguments}"

    generate_ask_extra_parameters = "Please fill some extra parameters needed for the template"
    could_not_find_any_templates = "Could not find any template with the given keyword. What to do next?"
    generate_keyword_argument = "Type the keyword you want to search for:"

    no_virtual_environment_remainder = "The current folder does not have a virtual environment in it."

    settings_ask_which_registry_delete = "Choose which registry to remove?"
    settings_python_use_system_default = "Use system default"
    settings_ask_python_version = "Choose the python version you want to use"
    settings_ask_template_version = "Choose the template version you want to use"
    settings_ask_local_template = "Choose the template you want to remove"
    settings_confirm_restore_defaults = "Confirm that you want to restore EVERY gryphon settings to the default?"
    settings_confirm_restorer_registry_defaults = "Confirm that you want to restore gryphon registry to the default?"

    settings_ask_registry_name = "Give a name to the new registry (ctrl+c to exit):"
    settings_confirm_remove_registry = "Confirm that you want to remove that registry from gryphon?"

    settings_ask_git_url = "Type the registry git url (i.e. https://github.com/your_github_user/your_github_repo):"
    settings_ask_local_path = "Type the registry path (i.e. /home/user/your_local_registry):"

    settings_confirm_change_env_manager = "Do you really want to change the environment manager to {env_manager}? "
    settings_confirm_registry_addition = "Confirm that you want to add the new {registry_name} registry to gryphon?"

    settings_confirm_new_template = "Confirm that you want to create a new template scaffolding inside the " \
                                    "folder '{location}'?"

    contact_us_type_question = "What would you like to do?"
