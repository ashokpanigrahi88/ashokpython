# CUSTOMER MANAGEMENT #
#
# DO NOT MODIFY CONSTANTS
CLIENT_SEGMENT_SAMPLE_1 = [
    {'first-name': 'Elsa', 'last-name': 'Frost', 'title': 'Princess',
     'address': '33 Castle Street, London', 'loyalty-program': 'Gold'},
    {'first-name': 'Anna', 'last-name': 'Frost', 'title': 'Princess',
     'address': '34 Castle Street, London', 'loyalty-program': 'Platinum'},
    {'first-name': 'Harry', 'middle-name': 'Harold', 'last-name': 'Hare',
     'title': 'Mr', 'email-address': 'harry.harold@hare.name',
     'loyalty-program': 'Silver'},
    {'first-name': 'Leonnie', 'last-name': 'Lion', 'title': 'Mrs',
     'loyalty-program': 'Silver'},
    ]


def preprocess_client_segment(segment):
    """This function simplifies a segment of clients to prepare for a marketing
    campaign. For each client in the segment, if the client has a registered
    address, it makes a tuple that contains the following details:
        - full name with title (e.g., "Mr John Smith") omitting any parts that
          are not provided,
        - full name includes title, first name, middle name and last name in
          that order if defined,
        - the mailing address (not the email-address).
    If a client has no registered addresses, he should not be included in the
    returned list.

    E.g., preprocess_client_segment(CLIENT_SEGMENT_SAMPLE_1)
    includes 'Princess Elsa Frost' but it should not include 'Mrs Leonnie
    Lion' because there are no associated addresses in the data.
    So, preprocess_client_segment(CLIENT_SEGMENT_SAMPLE_1)
    includes the tuple ('Princess Elsa Frost', '33 Castle Street, London')

    :param segment: list of client records. See sample above.
    :return: preprocessed list of tuples consisting of full name and mailing address.
    :rtype: list
    """

    if segment == []:
        return segment
    for customer in segment:
        ret = []
        fname = customer['first-name']
        lname = customer['last-name']
        try:
            middle = customer['middle-name']
            middle = middle+' '
        except KeyError:
            middle = ''
        try:
            title = customer['title']
            title = title+' '
        except KeyError:
            title = ''
        try:
            address = customer['address']
        except KeyError:
            address = 'NA'
        if address != 'NA':
            fullname = title+fname+' '+middle+lname
            ret.append((fullname, address))

        return ret


preprocess_client_segment([])
preprocess_client_segment([{'first-name': 'Elsa', 'last-name': 'Frost', 'title': 'Princess', 'loyalty-program': 'Gold'}, \
{'first-name': 'Anna', 'last-name': 'Frost', 'title': 'Princess', 'loyalty-program': 'Platinum'}, \
{'first-name': 'Harry', 'middle-name': 'Harold', 'last-name': 'Hare', 'title': 'Mr', 'email-address': 'harry.harold@hare.name', 'loyalty-program': 'Silver'}])
preprocess_client_segment([{'first-name': 'Elsa', 'last-name': 'Frost', 'title': 'Princess', 'address': '33 Castle Street, London', 'loyalty-program': 'Gold'}, {'first-name': 'Anna', 'last-name': 'Frost', 'title': 'Princess', 'loyalty-program': 'Platinum'}, {'first-name': 'Harry', 'middle-name': 'Harold', 'last-name': 'Hare', 'title': 'Mr', 'email-address': 'harry.harold@hare.name', 'loyalty-program': 'Silver'}])
preprocess_client_segment([{'first-name': 'Elsa', 'middle-name': 'Arundel', 'last-name': 'Frost', 'title': 'Princess', 'address': '33 Castle Street, London', 'loyalty-program': 'Gold'}])
preprocess_client_segment([{'first-name': 'Elsa', 'last-name': 'Frost', 'address': '33 Castle Street, London', 'loyalty-program': 'Gold'}])
