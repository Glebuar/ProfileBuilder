import xml.etree.ElementTree as ET
import os
import zipfile

def remove_question_suffix(question_type):
    return question_type.replace('Question', '')

def get_answer_value(question_type):
    if question_type == "static_fields":
        return {
            "status": "ExampleText",
            "jointClients": [
                {
                    "id": 1,
                    "clientId": "ExampleText",
                    "name": "ExampleText"
                }
            ],
            "jointClientNames": [
                "ExampleText"
            ],
            "jointClientIds": [
                1
            ],
            "clientId": "ExampleText",
            "createdBy": "ExampleText",
            "currentState": "ExampleText",
            "id": 1,
            "matterId": "ExampleText",
            "name": "ExampleText",
            "requestType": "ExampleText",
            "environment": "ExampleText",
            "progressStatus": "ExampleText",
            "createdById": 1,
            "clientName": "ExampleText",
            "matterName": "ExampleText",
            "lastStateExitedOn": "ExampleText",
            "formId": 1,
            "createdOn": "ExampleText",
            "modifiedOn": "ExampleText"
        }
    answer_mapping = {
        "AddressInput": {
            "addressType": "ExampleText",
            "city": "ExampleText",
            "contactName": "ExampleText",
            "country": "CA",
            "email": "ExampleText",
            "fax": "ExampleText",
            "phone": "ExampleText",
            "remoteId": "ExampleText",
            "state": "ExampleText",
            "streetAddress": ["ExampleText"],
            "title": "ExampleText",
            "webSite": "ExampleText",
            "zipCode": "ExampleText"
        },
        "RelatedPartiesInput": [
            {
                "name": "ExampleText",
                "notes": "ExampleText",
                "position": "ExampleText",
                "relationship": "ExampleText",
                "questionId": "ExampleText",
                "type": "ExampleText"
            }
        ],
        "PartyLookup": {
            "companyDetails": "ExampleText",
            "existingPartyId": 1,
            "existingPartyName": "ExampleText",
            "existingPartyEntityId": "ExampleText",
            "inputPartyName": "ExampleText",
            "partyId": "ExampleText",
            "partySystemId": 1,
            "id": 1
        },
        "CheckBoxListInput": [
            {
                "key": "ExampleText",
                "value": "ExampleText"
            }
        ],
        "ListBoxListInput": [
            {
                "key": "ExampleText",
                "value": "ExampleText"
            }
        ],
        "AutoCompleteMultiValueInput": [
            {
                "key": "ExampleText",
                "value": "ExampleText"
            }
        ],
        "DropdownListInput": {
            "key": "ExampleText",
            "value": "ExampleText"
        },
        "RadioButtonListInput": {
            "key": "ExampleText",
            "value": "ExampleText"
        },
        "AutoCompleteSingleValueInput": {
            "key": "ExampleText",
            "value": "ExampleText"
        },
        "BooleanRadioButtonInput": False,
        "BooleanCheckboxInput": False,
        "NumericInput": 1,
        "DateTimeInput": "ExampleText",      
        "TextInput": "ExampleText",
        "LabelInput": "ExampleText"
    }    
    return answer_mapping.get(question_type)

def parse_form_component_item(item):
    question_type = item.get('{http://www.w3.org/2001/XMLSchema-instance}type').split(':')[-1]
    question_type = remove_question_suffix(question_type)
    question_name_element = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}Name')
    if question_name_element is not None:
        question_name = question_name_element.text
        if question_name:
            question_name_lower = question_name.lower()
            answer_value = get_answer_value(question_type)
            if answer_value is not None:
                return {
                    question_name_lower: {
                        "name": question_name,
                        "type": question_type,
                        "answer": answer_value
                    }
                }
    return {}

def parse_sub_questions(sub_questions, column_import_mappings=None):
    questions = {}
    for sub_question in sub_questions.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfQuestionstringHQ4y65Wg'):
        key = sub_question.find('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Key')
        if key is not None:
            question_type = key.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            if question_type is None and column_import_mappings is not None:
                key_ref = key.get('{http://schemas.microsoft.com/2003/10/Serialization/}Ref')
                if key_ref is not None:
                    for column_mapping in column_import_mappings.findall('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}KeyValueOfQuestionColumnImportMappingMDdxSquB'):
                        column_key = column_mapping.find('{http://schemas.microsoft.com/2003/10/Serialization/Arrays}Key')
                        if column_key is not None and column_key.get('{http://schemas.microsoft.com/2003/10/Serialization/}Id') == key_ref:
                            key = column_key
                            question_type = key.get('{http://www.w3.org/2001/XMLSchema-instance}type')
                            break

            if question_type is not None:
                question_type = remove_question_suffix(question_type.split(':')[-1])
                question_name_element = key.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}Name')
                if question_name_element is not None:
                    question_name = question_name_element.text
                    if question_name:
                        question_name_lower = question_name.lower()
                        answer_value = get_answer_value(question_type)
                        if answer_value is not None:
                            questions[question_name_lower] = {
                                "name": question_name,
                                "type": question_type,
                                "value": answer_value
                            }
    return questions

def parse_multicolumn_list_item(item):
    question_name_element = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}Name')
    if question_name_element is not None:
        question_name = question_name_element.text
        if question_name:
            question_name_lower = question_name.lower()
            sub_questions = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}SubQuestionNames')
            column_import_mappings = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}ColumnImportMappings')
            if sub_questions is not None:
                questions = parse_sub_questions(sub_questions, column_import_mappings)
                if questions:
                    return {
                        question_name_lower: {
                            "name": question_name,
                            "type": "MultiColumnListInput",
                            "answer": {
                                "rows": [
                                    {
                                        "rowId": "0",
                                        "parentRowId": "0",
                                        "questions": questions
                                    }
                                ]
                            }
                        }
                    }
    return {}

def parse_section(section):
    section_name_element = section.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}Name')
    repeatable_group_id_element = section.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}RepeatableGroupId')

    section_name = section_name_element.text if section_name_element is not None else ""
    if repeatable_group_id_element is not None and repeatable_group_id_element.text and not section_name:
        return {}

    answers = {}
    questions_container = section.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}Questions')
    if questions_container is not None:
        questions = questions_container.findall('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms.Questions}Question')
        for question in questions:
            question_type = question.get('{http://www.w3.org/2001/XMLSchema-instance}type').split(':')[-1]
            question_type = remove_question_suffix(question_type)
            if question_type == 'MultiColumnListInput':
                question_answers = parse_multicolumn_list_item(question)
            else:
                question_answers = parse_form_component_item(question)
            if question_answers:
                answers.update(question_answers)

    if repeatable_group_id_element is not None and repeatable_group_id_element.text:
        if answers:
            repeatable_section = {
                section_name.lower(): {
                    "name": section_name,
                    "type": "RepeatableQuestionGroup",
                    "answer": {
                        "groups": [
                            {
                                "groupId": "0",
                                "questions": {k: {"name": v["name"], "type": v["type"], "value": v["answer"]} for k, v in answers.items()}
                            }
                        ]
                    }
                }
            }
            return repeatable_section
        else:
            return {}
    else:
        return answers

def parse_page(page):
    answers = {}    
    title_element = page.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}Title')
    if title_element is not None:
        title = title_element.text
        answers[f"SECTION - {title.upper()}"] = None
    items = page.findall('.//{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}FormComponentItem')
    for item in items:
        item_type = item.get('{http://www.w3.org/2001/XMLSchema-instance}type').split(':')[-1]
        item_type = remove_question_suffix(item_type)
        if item_type == 'Section':
            section_name_element = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}Name')
            section_name = section_name_element.text if section_name_element is not None else ""
            repeatable_group_id_element = item.find('{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}RepeatableGroupId')
            if repeatable_group_id_element is not None and repeatable_group_id_element.text and not section_name:
                continue
            section_answers = parse_section(item)
            if section_answers:
                answers.update(section_answers)
        elif item_type == 'MultiColumnListInput':
            item_answers = parse_multicolumn_list_item(item)
            if item_answers:
                answers.update(item_answers)
        else:
            item_answers = parse_form_component_item(item)
            if item_answers:
                answers.update(item_answers)
    return answers

def parse_form_definition(form_definition):
    answers = {}
    pages = form_definition.findall('.//{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}Page')
    for page in pages:
        page_answers = parse_page(page)
        answers.update(page_answers)
    return answers

def convert_xml_to_json(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    form_definitions = root.findall('.//{http://schemas.datacontract.org/2004/07/IntApp.Wilco.Model.Forms}FormDefinition')
    static_fields = get_answer_value("static_fields")
    json_output = {
        "answers": {},
        **static_fields
    }
    for form_definition in form_definitions:
        result = parse_form_definition(form_definition)
        json_output["answers"].update(result)
    return json_output

def extract_xml_from_zip(zip_path):
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        for file in zip_ref.namelist():
            if file.lower().endswith('.xml'):
                extracted_path = zip_ref.extract(file, os.path.dirname(zip_path))
                return extracted_path
    raise Exception("No XML file found in the IXT archive.")

def process_ixt_file(ixt_file):
    try:
        extracted_file = extract_xml_from_zip(ixt_file)
        result = convert_xml_to_json(extracted_file)
        return result, extracted_file
    except Exception as e:
        return None, None
