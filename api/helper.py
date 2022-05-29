from .models import Customer

# Helper Function to valid phone number
def valid_number(number: str) -> list:
    bugs = []

    if Customer.objects.all().filter(phone_number = number):
        bugs.append('taken')

    try:
        int(number)
    except:
        bugs.append('not_a_number')
    
    if not number:
        bugs.append('blank')

    elif number[0] == '0' and len(number) == 11:
        pass

    elif number[0] == '0' and len(number) < 11:
        bugs.append('too_short')
        bugs.append('10')

    elif number[0] == '0' and len(number) > 11:
        bugs.append('too_long')
        bugs.append('15')
        
    else:
        pass

    return bugs
        

