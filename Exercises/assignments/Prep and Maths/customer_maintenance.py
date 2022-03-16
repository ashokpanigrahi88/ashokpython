# CUSTOMER MANAGEMENT #
#
# DO NOT MODIFY CONSTANTS
CLIENT_SEGMENT_SAMPLE_1 = [
    {
        'first-name': 'Elsa',
        'last-name': 'Frost',
        'title': 'Princess',
        'address': '33 Castle Street, London',
        'loyalty-program': 'Gold'
    },
    {
        'first-name': 'Anna',
        'last-name': 'Frost',
        'title': 'Princess',
        'address': '34 Castle Street, London',
        'loyalty-program': 'Platinum'
    },
    {
        'first-name': 'Harry',
        'middle-name': 'Harold',
        'last-name': 'Hare',
        'title': 'Mr',
        'email-address': 'harry.harold@hare.name',
        'loyalty-program': 'Silver'
    },
    {
        'first-name': 'Leonnie',
        'last-name': 'Lion',
        'title': 'Mrs',
        'loyalty-program': 'Silver'
    },
]


def _preprocess_one_client(client):
    """
    :param client:
    :return:
    :rtype:
    """
    if 'address' in client.keys():
        name_chunks = [
            client.get('title'),
            client.get('first-name'),
            client.get('middle-name'),
            client.get('last-name')
        ]
        name_chunks_not_none = [c for c in name_chunks if c is not None]
        name = ' '.join(name_chunks_not_none)
        address = client.get('address')
        return (name, address)
    else:
        return None


def preprocess_client_segment(segment):
    """This function simplifies a segment of clients to prepare for a marketing
    campaign. For each client in the segment, if the client has a registered
    address, it makes a tuple that contains the following details:
        - full name with title (e.g., "Mr John Smith") omitting any part that
          are not provided,
        - full name includes title, first name, middle name and last name in
          that order if defined
        - the mailing address (not the email-address).
    If a client has no registered address, it should not be included in the
    returned list.

    E.g., preprocess_segment_for_marketing_campaign(CLIENT_SEGMENT_SAMPLE_1)
    inlcudes 'Princess Elsa Frost' but it should not include 'Mrs Leonnie
    Lion' because there are no associated addresses in the data.
    Ans so, preprocess_segment_for_marketing_campaign(CLIENT_SEGMENT_SAMPLE_1)
    includes the tuple ('Princess Elsa Frost', '33 Castle Street, London')

    :param segment: list of client records. See sample above.
    :return: preprocessed list of tuples consisting of full name and mailing address.
    :rtype: list
    """

    summaries = [_preprocess_one_client(client) for client in segment]
    summaries_not_none = [s for s in summaries if s is not None]
    return summaries_not_none
