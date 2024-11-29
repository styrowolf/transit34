# remove excessive whitespaces https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string/15913564#15913564
# double spaces and trimming
def clean_str(text: str) -> str:
    if text is None:
        return None
    return " ".join(text.split())

def false_if_none(value: bool) -> bool:
    if value is None:
        return False
    else:
        return value
    
def extract_line_code_from_route_code(route_code: str) -> str:
    return route_code.split("_")[0]