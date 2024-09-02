import json

import requests
from bs4 import BeautifulSoup
# try:
from html import unescape  # python 3.4+


def login_to_website(login_url):
    # Start a session to maintain cookies
    session = requests.Session()

    # Step 1: Get the login page to retrieve the authenticity_token
    login_page = session.get(login_url)
    soup = BeautifulSoup(login_page.text, 'html.parser')

    # Step 2: Extract the authenticity_token from the login page
    authenticity_token = soup.find('input', {'name': 'authenticity_token'})['value']

    # Step 3: Define the login payload with the retrieved authenticity_token
    payload = {
        'authenticity_token': authenticity_token,
        'user[email]': 'bharath@morphle.in',
        'user[password]': 'Morphleiswow1',
        'commit': 'Log in'
    }
    # Step 4: Perform the login
    login_response = session.post(login_url, data=payload)

    # Check if login was successful
    if login_response.status_code == 200:
        return session
    else:
        raise Exception("Not able to login")


def get_data_of_record_in_markdown(data_url, session):
    # for data_url in urls:
    # Step 5: Access the data page after successful login
    data_response = session.get('https://app.openregulatory.com'+data_url+'/edit')
    #
    if data_response.status_code == 200:
        # Parse the page content
        soup = BeautifulSoup(data_response.content, 'html.parser')
        # print(soup)

        # Find the starting and ending elements
        start_tag = soup.find('div', {'data-toastui-editor-target': 'container'})
        end_tag = soup.find('input', {'id': 'record_template_id'})

        # Initialize a list to collect the content
        content = []

        if start_tag and end_tag:
            # Start extracting content after the start_tag
            current = start_tag.find_next_sibling()

            while current and current != end_tag:
                # Append the content of the current element
                content.append(str(current))
                # Move to the next sibling
                current = current.find_next_sibling()

            # Join content into a single string
            result = '\n'.join(content)

            # print('Title: '+result.split('&lt;/span&gt;')[0].split('Title: ')[1])
            # print(unescape(result.split('"/>')[0].split('Title: ')[1]))

            try:
                value = unescape(result.split('"/>')[0].split('Title: ')[1])
            except:
                value = unescape(result)
            return value

        # Customize this part to extract the specific data you need
    else:
        print("Failed to retrieve the data page.")


# def get_folder_urls_of_scanner_folders(url, session):
#     data_response = session.get(url)
#     if data_response.status_code == 200:
#         soup = BeautifulSoup(data_response.content, 'html.parser')
#         # print(soup)
#         folder_names = [p.text.strip() for p in soup.find_all('p', class_='text-lg font-semibold')]
#
#         form_elements = soup.find_all('form', {'data-folder-id': True})
#         data_folder_ids = [form['data-folder-id'] for form in form_elements]
#
#         print(folder_names)
#         print(data_folder_ids)
#
#         dict_vals={}
#         if len(folder_names) == len(data_folder_ids):
#             for i in range(len(folder_names)):
#                 dict_vals[folder_names[i]]=data_folder_ids[i]
#         print(dict_vals)
#
#     else:
#         print("Failed to retrieve the data page.")


def get_folder_urls_of_scanner_folders(url, session):
    data_response = session.get(url)
    if data_response.status_code == 200:
        soup = BeautifulSoup(data_response.content, 'html.parser')
        folder_names = [p.text.strip() for p in soup.find_all('p', class_='text-lg font-semibold')]
        form_elements = soup.find_all('form', {'data-folder-id': True})
        data_folder_ids = [form['data-folder-id'] for form in form_elements]
        dict_vals = {}
        if len(folder_names) == len(data_folder_ids):
            for i in range(len(folder_names)):
                dict_vals[folder_names[i]] = {'scanner_url': data_folder_ids[i]}
        return dict_vals
    else:
        print("Failed to retrieve the data page.")
        return None

def get_all_docs(url, session):
    data_response = session.get(url)
    if data_response.status_code == 200:
        soup = BeautifulSoup(data_response.content, 'html.parser')
        folder_names = [p.text.strip() for p in soup.find_all('p', class_='text-lg font-semibold')]
        form_elements = soup.find_all('form', {'data-folder-id': True})
        data_folder_ids = [form['data-folder-id'] for form in form_elements]
        dict_vals = {}
        if len(folder_names) == len(data_folder_ids):
            for i in range(len(folder_names)):
                dict_vals[folder_names[i]] = {'scanner_url': data_folder_ids[i]}
        return dict_vals
    else:
        print("Failed to retrieve the data page.")
        return None

def get_record_urls_of_individual_folders(folder_urls_of_scanner_folders, session):
    for folder_name, folder_info in folder_urls_of_scanner_folders.items():
        dict_vals = []
        scanner_url = folder_info['scanner_url']
        # print(f"Folder Name: {folder_name}, Scanner URL: {scanner_url}")
        data_response = session.get('https://app.openregulatory.com/folders/'+scanner_url)
        if data_response.status_code == 200:
            soup = BeautifulSoup(data_response.content, 'html.parser')
            # print(soup)
            form_elements = soup.find_all('form', {'data-folder-id': True})
            data_folder_ids = [form['data-folder-id'] for form in form_elements]
            a_tags = soup.find_all('a', class_='block', href=True)
            # Iterate through each <a> tag
            for a_tag in a_tags:
                href_value = a_tag['href']
                p_tag = a_tag.find('p', class_='font-semibold text-lg')  # Find the specific <p> tag inside the <a> tag
                if p_tag:
                    text_value = p_tag.text
                    dict_vals.append({"Title": text_value, "Markdown": get_data_of_record_in_markdown(href_value, session)})
            # print(data_folder_ids)
        else:
            print("Failed to retrieve the data page.")


        scanner_url = folder_info['scanner_url']
        # print(f"Folder Name: {folder_name}, Scanner URL: {scanner_url}")
        data_response = session.get('https://app.openregulatory.com/folders/' + scanner_url)
        if data_response.status_code == 200:
            soup = BeautifulSoup(data_response.content, 'html.parser')
            form_elements = soup.find_all('form', {'data-folder-id': True})
            data_folder_ids = [form['data-folder-id'] for form in form_elements]
            if (len(data_folder_ids) > 0):
                for data_folder_id in data_folder_ids:
                    data_response = session.get('https://app.openregulatory.com/folders/' + data_folder_id)
                    if data_response.status_code == 200:
                        soup = BeautifulSoup(data_response.content, 'html.parser')
                        a_tags = soup.find_all('a', class_='block', href=True)
                        # Iterate through each <a> tag
                        for a_tag in a_tags:
                            href_value = a_tag['href']
                            p_tag = a_tag.find('p', class_='font-semibold text-lg')  # Find the specific <p> tag inside the <a> tag
                            if p_tag:
                                text_value = p_tag.text
                                dict_vals.append({"Title": text_value, "Markdown": get_data_of_record_in_markdown(href_value, session)})
            # print(data_folder_ids)
        else:
            print("Failed to retrieve the data page.")
        folder_urls_of_scanner_folders[folder_name]= {'Scanner Content': dict_vals}

    dict_vals_json = json.dumps(folder_urls_of_scanner_folders, indent=4)

    # Specify the filename
    filename = '/home/morphle/Desktop/output.json'

    # Write the JSON string to the file
    with open(filename, 'w') as file:
        file.write(dict_vals_json)


if __name__ == '__main__':
    # Define the URL and login credentials
    login_url = 'https://app.openregulatory.com/users/sign_in'  # Replace with actual login URL
    scanner_type_urls=['https://app.openregulatory.com/folders/0b49af69-1b4d-431a-8379-967431f9bd02?sort=az']

    session = login_to_website(login_url)
    for scanner_type_url in scanner_type_urls:
        folder_urls_of_scanner_folders = get_folder_urls_of_scanner_folders(scanner_type_url, session)
        get_record_urls_of_individual_folders(folder_urls_of_scanner_folders, session)
