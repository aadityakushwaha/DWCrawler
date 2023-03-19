def create_string_from_data(data):
            string = ""
            
            # Add the title to the string
            if data['title']:
                string += data['title'] + "\n\n"
            
            # Add the meta content to the string
            if data['meta_content']:
                for key, value in data['meta_content'].items():
                    string += key + ": " + value + "\n"
                string += "\n"
            
            # Add the headings to the string
            if data['headings']:
                for heading in data['headings']:
                    string += heading + "\n"
                string += "\n"
            
            # Add the paragraphs to the string
            if data['paragraphs']:
                for paragraph in data['paragraphs']:
                    string += paragraph + "\n\n"
            
            # Add the links to the string
            if data['links']:
                string += "Links:\n"
                for link in data['links']:
                    string += link['href'] + "\n"
                string += "\n"
            
            # Add the image links to the string
            if data['image_links']:
                string += "Image Links:\n"
                for link in data['image_links']:
                    string += link + "\n"
                string += "\n"
            
            return string.strip()