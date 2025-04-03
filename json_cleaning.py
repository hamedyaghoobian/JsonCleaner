import json
import re
import os

def extract_name_and_position(text):
    original_text = text
    
    # Extract phone number if present
    phone_pattern = r'(?:\(?\d{3}\)?[-\s]?\d{3}[-\s]?\d{4})'
    phone_match = re.search(phone_pattern, text)
    phone = phone_match.group(0) if phone_match else ""
    
    # Remove phone from text for easier parsing
    if phone:
        text = text.replace(phone, "").strip()
    
    # Remove any social media handles or usernames
    text = re.sub(r'@\S+', '', text).strip()
    text = re.sub(r'(?<!\S)[a-z]+_[a-z]+(?!\S)', '', text, flags=re.IGNORECASE).strip()
    
    # Remove year references like '19, '22, etc.
    text = re.sub(r"'\d{2}", "", text).strip()
    
    # Special handling for entries with position-like terms in the middle
    position_terms = ["Head", "Assistant", "Associate", "Director", "Coach", "Volunteer", "Graduate"]
    
    # Check if any position term appears in the middle of the text
    for term in position_terms:
        match = re.search(fr'([A-Za-z\s]+)\s+{term}\s+([A-Za-z\s\']+)', text)
        if match:
            name_parts = match.group(1).strip().split()
            if len(name_parts) <= 2:  # Likely just first and last name
                full_name = match.group(1).strip()
                position = f"{term} {match.group(2)}".strip()
                break
    else:
        # Special case for coach positions with specialized roles
        special_coach_pattern = r'(.*?)\s+(Pitching|Assistant|Associate|Head|Volunteer|Graduate|Goalkeeping|Goalkeeper|Defensive|Offensive)\s+Coach(.*)$'
        special_match = re.search(special_coach_pattern, text, re.IGNORECASE)
        if special_match:
            full_name = special_match.group(1).strip()
            position = (special_match.group(2) + " Coach" + special_match.group(3)).strip()
        else:
            # Try to identify position by looking for common position titles
            position_patterns = [
                r'(.*?)(Head Coach|Director of|Director|Coordinator|Manager|Analyst)(.*)$',
                r'(.*?)(Coach)(.*)$'
            ]
            
            for pattern in position_patterns:
                match = re.search(pattern, text, re.IGNORECASE)
                if match:
                    full_name = match.group(1).strip()
                    position = (match.group(2) + (match.group(3) or "")).strip()
                    break
            else:
                # Fallback: assume format is "FirstName LastName Position"
                parts = text.split()
                if len(parts) >= 3:
                    # Assume first two words are name and rest is position
                    name_parts = parts[:2]
                    position_parts = parts[2:]
                    full_name = " ".join(name_parts)
                    position = " ".join(position_parts)
                else:
                    # If only 1-2 words, assume it's just a name
                    full_name = text
                    position = ""
    
    # Extract first and last name
    name_parts = full_name.split()
    first_name = name_parts[0] if name_parts else ""
    last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
    
    return {
        "full_name": full_name,
        "position": position,
        "phone": phone,
        "first_name": first_name,
        "last_name": last_name
    }

def process_staff_directory(school_data):
    school_name = school_data["name"].replace("- done", "").strip()
    staff_directory = school_data.get("staff_directory", [])
    
    results = []
    current_sport = ""
    
    for item in staff_directory:
        text = item.get("text", "").strip()
        email = item.get("email", "")
        
        # Skip empty entries
        if not text:
            continue
            
        # Check if this is a sport header
        if len(text.split()) <= 4 and not re.search(r'\d', text) and not email:
            current_sport = text
            continue
        
        # Process staff member
        person_info = extract_name_and_position(text)
        
        # Create the person entry
        person = {
            "school": school_name,
            "sport": current_sport,
            "full_name": person_info["full_name"],
            "position": person_info["position"],
            "phone": person_info["phone"],
            "email": email,
            "first_name": person_info["first_name"],
            "last_name": person_info["last_name"]
        }
        
        results.append(person)
    
    return results

def main():
    input_file = "data/ncaa_finished_schools_part_1.json"
    output_file = "data/transformed_staff_directory.json"
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    all_staff = []
    
    for school in data:
        staff = process_staff_directory(school)
        all_staff.extend(staff)
    
    # Write the result to a new file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_staff, f, indent=4)
    
    print(f"Processed {len(data)} schools with {len(all_staff)} staff members")
    print(f"Results saved to {output_file}")

if __name__ == "__main__":
    main() 