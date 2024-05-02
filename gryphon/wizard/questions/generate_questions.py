import questionary
from questionary import Choice, Separator
from .common_functions import base_question, base_text_prompt, get_back_choice
from ..wizard_text import Text
from ...constants import (QUIT, YES, NO, TYPE_AGAIN, READ_MORE, LOCAL_TEMPLATE,
                          USE_CASES, METHODOLOGY, TOPIC, SECTOR, DOWNLOAD, EMAIL_APPROVER, MMC_GITHUB_SETUP)

import logging
logger = logging.getLogger('gryphon')


class GenerateQuestions:

    @staticmethod
    @base_question
    def get_generate_option(categories: list, context = None):
        categories = categories.copy()
        
        if context is not None:
            # Context is available
        
            if (context.get("history") is None) or (len(context.get("history")) == 0):
                pass
                
            elif context["history"][0] == METHODOLOGY:
                
                if len(context["history"]) == 1:
                    for idx, category in enumerate(categories):
                        
                        counter = 0
                        for name, template in context["templates"].items():
                            if category in template.methodology:
                                counter += 1
                        
                        if counter != 1:
                            categories[idx] = category + " | " + str(counter) + " templates"
                        else:
                            categories[idx] = category + " | " + str(counter) + " template" 
            
            elif context["history"][0] == USE_CASES:
                
                if len(context["history"]) == 1:
                    pass
                
                elif (len(context["history"]) == 2) and (context["history"][1] in [TOPIC, SECTOR]):
                    
                    for idx, category in enumerate(categories):
                        
                        counter = 0
                        for name, template in context["templates"].items():
                            if (context["history"][1] == TOPIC) and (category in template.topic):
                                counter += 1
                            elif (context["history"][1] == SECTOR) and (category in template.sector):
                                counter += 1
                        
                        if counter != 1:
                            categories[idx] = category + " | " + str(counter) + " templates"
                        else:
                            categories[idx] = category + " | " + str(counter) + " template"
                
        categories.extend([
            Separator(Text.menu_separator),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.add_prompt_categories_question,
            choices=categories,
            # choices=dict(zip([str(x) + " AA" for x in categories], categories)), # DOES NOT WORK
            instruction=Text.add_prompt_instruction
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_which_template(metadata):
        options = [
            Choice(
                title=f"{template.display_name} "
                      + (f"(local template)" if template.registry_type == LOCAL_TEMPLATE else "") + (f"(Standalone download)" if template.command == DOWNLOAD else ""),

                value=name
            )
            for name, template in metadata.items()
        ]

        options.extend([
            Separator(Text.menu_separator),
            get_back_choice()
        ])

        return questionary.select(
            message=Text.generate_prompt_template_question,
            choices=options
        ).unsafe_ask()

    @staticmethod
    @base_question
    def ask_extra_arguments(arguments: list):
        extra_questions = [
            dict(
                type='input',
                name=field['name'],
                message=field['help']
            )
            for field in arguments
        ]
        return questionary.unsafe_prompt(extra_questions)

    @staticmethod
    @base_question
    def confirm_generate(template_name, read_more_option=False, approval_required=False, **kwargs):

        information = Text.generate_confirm_1.replace("{template_name}", template_name)
        information += (
            Text.generate_confirm_2.replace("{arguments}", str(kwargs))
            if len(kwargs) else ""
        )

        choices = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]
        if read_more_option:
            choices.append(
                Choice(
                    title="Read more",
                    value=READ_MORE
                )
            )
        if approval_required:
            choices.append(
                Choice(
                    title="Email approver",
                    value=EMAIL_APPROVER
                )
            )
            choices.append(
                Choice(
                    title="Get set up with MMC GitHub",
                    value=MMC_GITHUB_SETUP
                )
            )

        return questionary.select(
            message=information,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def confirm_generate_all():

        information = Text.generate_all_confirm

        choices = [
            Choice(
                title="Yes",
                value=YES
            ),
            Choice(
                title="No",
                value=NO
            )
        ]

        return questionary.select(
            message=information,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_text_prompt
    def generate_keyword_question():
        return questionary.text(message=Text.generate_keyword_argument).unsafe_ask()

    @staticmethod
    @base_question
    def nothing_found():
        choices = [
            get_back_choice(),
            Choice(
                title="Quit",
                value=QUIT
            ),
        ]

        return questionary.select(
            message=Text.could_not_find_any_templates,
            choices=choices
        ).unsafe_ask()

    @staticmethod
    @base_question
    def nothing_found_typing():
        choices = [
            Choice(
                title="Try another keyword",
                value=TYPE_AGAIN
            ),
            Separator(),
            get_back_choice(),
            Choice(
                title="Quit",
                value=QUIT
            ),
        ]

        return questionary.select(
            message=Text.could_not_find_any_templates,
            choices=choices
        ).unsafe_ask()
