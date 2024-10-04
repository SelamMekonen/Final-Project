import numpy as np
import pandas as pd
import tldextract
import math
from urllib.parse import urlparse
import os
from sklearn.preprocessing import StandardScaler
import requests
from bs4 import BeautifulSoup
import re


## -------------------------------------------- PATTERNS ------------------------------------------------------------

ipv4_pattern = r"^(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)$"
ipv6_pattern = (
    r"^(?:(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){6})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):"
    r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}"
    r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:::(?:(?:(?:[0-9a-fA-F]{1,4})):){5})"
    r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|"
    r"(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|"
    r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){4})"
    r"(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|"
    r"(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|"
    r"(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,1}(?:(?:[0-9a-fA-F]{1,4})))?::"
    r"(?:(?:(?:[0-9a-fA-F]{1,4})):){3})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|"
    r"(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}"
    r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,2}"
    r"(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:(?:[0-9a-fA-F]{1,4})):){2})(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):"
    r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|"
    r"(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,3}"
    r"(?:(?:[0-9a-fA-F]{1,4})))?::(?:(?:[0-9a-fA-F]{1,4})):)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):"
    r"(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}"
    r"(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,4}"
    r"(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):(?:(?:[0-9a-fA-F]{1,4})))|"
    r"(?:(?:(?:(?:(?:25[0-5]|(?:[1-9]|1[0-9]|2[0-4])?[0-9]))\.){3}(?:(?:25[0-5]|"
    r"(?:[1-9]|1[0-9]|2[0-4])?[0-9])))))))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,5}"
    r"(?:(?:[0-9a-fA-F]{1,4})))?::)(?:(?:[0-9a-fA-F]{1,4})))|(?:(?:(?:(?:(?:(?:[0-9a-fA-F]{1,4})):){0,6}"
    r"(?:(?:[0-9a-fA-F]{1,4})))?::))))$"
)
shortening_services = (
    r"bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|"
    r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|"
    r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|"
    r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|t\.co|lnkd\.in|db\.tt|"
    r"qr\.ae|adf\.ly|goo\.gl|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|bit\.ly|ity\.im|q\.gs|is\.gd|"
    r"po\.st|bc\.vc|twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|x\.co|"
    r"prettylinkpro\.com|scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|"
    r"tr\.im|link\.zip\.net"
)
http_https = r"https://|http://"

###############################################################################################################################################################


def entropy(str):
    # p, lns = Counter(s), float(len(s))
    # return -sum( count/lns * math.log(count/lns, 2) for count in p.values())
    # alphabet = string.ascii_lowercase
    # alphabet_letters = list (alphabet)

    unique_chars = set(str)
    entropy = 0

    for char in unique_chars:
        if char.isalpha():
            p_i = float(str.count(char)) / len(str)
            entropy -= p_i * math.log(p_i, 10)
        else:
            continue

    return entropy


def get_number_rate_after_path(url):
    after_path_str = url.split("/")[-1]  # Last element in the splitup url
    if not after_path_str:
        return -1

    count_digits_after_path_str = sum(c.isdigit() for c in after_path_str)

    return count_digits_after_path_str / len(after_path_str)


def get_character_continuity_rate(domain):
    # longest token (consecutive) for each character type
    longest_letter_token = 0
    longest_digit_token = 0
    longest_symbol_token = 0

    # Current count of consecutive characters
    count_letter = 0
    count_digit = 0
    count_symbol = 0

    for c in domain:
        if c.isalpha():
            count_letter += 1
            # resetting
            count_digit = 0
            count_symbol = 0
            if count_letter > longest_letter_token:
                longest_letter_token = count_letter

        elif c.isdigit():
            count_digit += 1
            count_letter = 0
            count_symbol = 0
            if count_digit > longest_digit_token:
                longest_digit_token = count_digit

        # c is a symbol
        else:
            count_symbol += 1
            count_digit = 0
            count_letter = 0
            if count_symbol > longest_symbol_token:
                longest_symbol_token = count_symbol

    char_continuity_rate = float(
        longest_digit_token + longest_letter_token + longest_symbol_token
    ) / len(domain)

    return char_continuity_rate


def get_number_rate_url(url):
    url_parts = url.split("/")

    count_digits = 0
    for component in url_parts:
        count_digits += sum(c.isdigit() for c in component)

    return count_digits / len(url)


def get_avg_pathtoken_len(parsed_url):
    path_tokens_list = parsed_url.path.split("/")

    if not path_tokens_list:
        return 0

    total_length_of_tokens_in_path_list = sum(len(token) for token in path_tokens_list)

    avg_token_length_in_path_list = total_length_of_tokens_in_path_list / len(
        path_tokens_list
    )

    return avg_token_length_in_path_list


def is_IP_in_URL(url):
    regex = r"\d{1,3}[\.]{1}\d{1,3}[\.]{1}\d{1,3}[\.]{1}\d{1,3}"
    if re.search(regex, url) is None:
        return -1
    else:
        return 1


def is_long_URL(url):
    if len(url) < 54:
        return -1
    elif len(url) >= 54 and len(url) <= 75:
        return 0
    else:
        return 1


def is_tiny_URL(url):
    if len(url) > 20:
        return -1
    else:
        return 1


def is_redirecting_URL(url):
    reg1 = re.compile("^http:")
    reg2 = re.compile("^https:")
    srch = "//"
    if url.find(srch) == 5 and reg1.search(url) and not re.search(srch, url[7:]):
        return -1
    elif url.find(srch) == 6 and reg2.search(url) and not re.search(srch, url[8:]):
        return -1
    else:
        return 1


def is_hyphen_URL(url):
    reg = re.compile("[a-zA-Z]\\/").pattern
    srch = "-"
    if not re.search(srch, url[: url.find(reg) + 1]):
        return -1
    else:
        return 1


def is_multi_domain_URL(url):
    reg = "[a-zA-Z]\\/"
    if len(url[: url.find(reg) + 1].split(".")) < 5:
        return -1
    else:
        return 1


# def isFaviconDomainUnidentical(url):

#     url = requests.get(url).text
#     soup = BeautifulSoup(url, 'html.parser')

#     favicon = soup.find('link', rel='shortcut icon')
#     if favicon:
#         favicon_url = favicon['href']
#         parsed_url = urlparse(url)
#         parsed_favicon_url = urlparse(favicon_url)

#         if re.search(r'[a-zA-Z]/', parsed_favicon_url.path):
#             domain = parsed_url.netloc.split('.')
#             favicon_domain = parsed_favicon_url.netloc.split('.')

#             if domain != favicon_domain:
#                 return 1

#     return -1


def isIllegalHttpsURL(url):
    srch1 = "//"
    srch2 = "https"

    if srch1 in url and srch2 not in url[url.index(srch1) :]:
        return -1
    else:
        return 1


def is_alpha_numeric_URL(url):
    search = "@"
    if search not in url:
        return -1
    else:
        return 1


def request_url(url, domain):
    r = requests.get(url)

    soup = BeautifulSoup(r.content, "html.parser")

    i = 0
    success = 0
    for img in soup.find_all("img", src=True):
        dots = [x.start() for x in re.finditer(r"\.", img["src"])]
        if url in img["src"] or domain in img["src"] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for audio in soup.find_all("audio", src=True):
        dots = [x.start() for x in re.finditer(r"\.", audio["src"])]
        if url in audio["src"] or domain in audio["src"] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for embed in soup.find_all("embed", src=True):
        dots = [x.start() for x in re.finditer(r"\.", embed["src"])]
        if url in embed["src"] or domain in embed["src"] or len(dots) == 1:
            success = success + 1
        i = i + 1

    for i_frame in soup.find_all("i_frame", src=True):
        dots = [x.start() for x in re.finditer(r"\.", i_frame["src"])]
        if url in i_frame["src"] or domain in i_frame["src"] or len(dots) == 1:
            success = success + 1
        i = i + 1

    try:
        percentage = success / float(i) * 100
    except:
        return 1

    if percentage < 22.0:
        return 1
    elif 22.0 <= percentage < 61.0:
        return 0
    else:
        return -1


def prefix_suffix(domain):
    match = re.search("-", domain)
    return -1 if match else 1


def dns(domain):
    domain_reachable = 1
    try:
        domain_verified = whois.query(domain)
    except:
        domain_reachable = -1

    return domain_reachable


def having_ip_address(url):
    ip_address_pattern = ipv4_pattern + "|" + ipv6_pattern
    match = re.search(ip_address_pattern, url)
    return -1 if match else 1


# Feature 5
def double_slash_redirecting(url):
    # since the position starts from 0, we have given 6 and not 7 which is according to the document.
    # It is convenient and easier to just use string search here to search the last occurrence instead of re.
    last_double_slash = url.rfind("//")
    return -1 if last_double_slash > 6 else 1


def https_token(url):
    match = re.search(http_https, url)
    if match and match.start() == 0:
        url = url[match.end() :]
    match = re.search("http|https", url)
    return -1 if match else 1


def having_sub_domain(url):
    if having_ip_address(url) == -1:
        match = re.search(
            "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
            "([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}",
            url,
        )
        pos = match.end()
        url = url[pos:]
    num_dots = [x.start() for x in re.finditer(r"\.", url)]
    if len(num_dots) <= 3:
        return 1
    elif len(num_dots) == 4:
        return 0
    else:
        return -1


# ------------------------------ main extractor --------------------
def extract_features(url):
    parsed_url = urlparse(url)

    tld_ext = tldextract.extract(url)
    if tld_ext.subdomain != "":
        domain = tld_ext.subdomain + "." + tld_ext.domain + "." + tld_ext.suffix
    else:
        domain = tld_ext.domain + "." + tld_ext.suffix

    args = parsed_url.query
    path = parsed_url.path
    filename = os.path.basename(parsed_url.path)

    Entropy_Domain = entropy(domain)
    argPathRatio = len(args) / len(path) if path else -1
    ArgUrlRatio = len(args) / len(url)
    argDomanRatio = len(args) / len(domain)
    pathurlRatio = len(path) / len(url)
    CharacterContinuityRate = get_character_continuity_rate(domain)
    NumberRate_FileName = (
        sum(c.isdigit() for c in filename) / len(filename) if filename else -1
    )
    domainUrlRatio = len(domain) / len(url)
    NumberRate_URL = get_number_rate_url(url)
    PathDomainRatio = len(path) / len(domain)
    NumberRate_AfterPath = get_number_rate_after_path(url)
    avgpathtokenlen = get_avg_pathtoken_len(parsed_url)
    is_ip_exist = is_IP_in_URL(url)
    is_long = is_long_URL(url)
    is_tiny = is_tiny_URL(url)
    is_alphanumeric = is_alpha_numeric_URL(url)
    is_redirecting = is_redirecting_URL(url)
    # is_hyphenated = is_hyphen_URL(url)
    # is_multi_domain = is_multi_domain_URL(url)
    is_hyphen_domain = prefix_suffix(domain)
    # is_request_success = request_url(url, domain)
    double_slash = double_slash_redirecting(url)
    http_in_domain = https_token(url)
    sub_domain = having_sub_domain(url)
    isIllegalHttps = isIllegalHttpsURL(url)

    # features = np.array([[Entropy_Domain, argPathRatio, ArgUrlRatio, argDomanRatio, pathurlRatio,
    #                       CharacterContinuityRate, NumberRate_FileName, domainUrlRatio,
    #                       NumberRate_URL, PathDomainRatio, NumberRate_AfterPath, avgpathtokenlen]])

    features = [
        Entropy_Domain,
        CharacterContinuityRate,
        NumberRate_FileName,
        domainUrlRatio,
        NumberRate_URL,
        PathDomainRatio,
        NumberRate_AfterPath,
        avgpathtokenlen,
        is_ip_exist,
        is_long,
        is_tiny,
        is_alphanumeric,
        is_redirecting,
        is_hyphen_domain,
        isIllegalHttps,
        double_slash,
        http_in_domain,
        sub_domain,
    ]  # pathurlRatio

    return features


def read_data(file_dir):
    # For testing (Will optimize later)
    df_data = pd.read_csv(file_dir)
    urls = []
    labels = []

    Entropy_Domain = []
    argPathRatio = []
    ArgUrlRatio = []
    argDomanRatio = []
    pathurlRatio = []
    CharacterContinuityRate = []
    NumberRate_FileName = []
    domainUrlRatio = []
    NumberRate_URL = []
    PathDomainRatio = []
    NumberRate_AfterPath = []
    avgpathtokenlen = []
    is_ip_exist = []
    is_long = []
    is_tiny = []
    is_alphanumeric = []
    is_redirecting = []
    is_hyphenated = []
    is_multi_domain = []
    isIllegalHttps = []
    request_url = []
    prefix_suffix = []
    sub_domains = []
    http_tokens = []
    double_slash = []

    for row in df_data.itertuples(index=False):
        label = row[-1]
        if label == 1:
            labels.append(1)
        else:
            labels.append(0)

        url = row[1]
        urls.append(url)

        features = extract_features(url)

        Entropy_Domain.append(features[0])
        # argPathRatio.append(features[1])
        # ArgUrlRatio.append(features[1])
        # argDomanRatio.append(features[2])
        # pathurlRatio.append(features[3])
        CharacterContinuityRate.append(features[1])
        NumberRate_FileName.append(features[2])
        domainUrlRatio.append(features[3])
        NumberRate_URL.append(features[4])
        PathDomainRatio.append(features[5])
        NumberRate_AfterPath.append(features[6])
        avgpathtokenlen.append(features[7])
        is_ip_exist.append(features[8])
        is_long.append(features[9])
        is_tiny.append(features[10])
        is_alphanumeric.append(features[11])
        is_redirecting.append(features[12])
        prefix_suffix.append(features[13])
        # request_url.append(features[14])
        isIllegalHttps.append(features[14])
        double_slash.append(features[15])
        http_tokens.append(features[16])
        sub_domains.append(features[17])
        pathurlRatio.append(features[18])

    df_features = pd.DataFrame(
        {
            "a": Entropy_Domain,
            "f": CharacterContinuityRate,
            "g": NumberRate_FileName,
            "h": domainUrlRatio,
            "i": NumberRate_URL,
            "j": PathDomainRatio,
            "k": NumberRate_AfterPath,
            "l": avgpathtokenlen,
            "m": is_ip_exist,
            "n": is_long,
            "o": is_tiny,
            "p": is_alphanumeric,
            "q": is_redirecting,
            "r": prefix_suffix,
            "s": isIllegalHttps,
            "t": double_slash,
            "u": http_tokens,
            "v": sub_domains,
        }
    )  # 's':request_url ,yy

    df_labels = pd.DataFrame(labels)

    X = df_features.to_numpy()
    scaler = StandardScaler()
    scaler.fit(X)
    df_scaled = pd.DataFrame(scaler.transform(X), columns=df_features.columns)

    df_features.to_csv("/Users/sg/Desktop/Betty/dataset/dataset.csv")
    df_scaled.to_csv("/Users/sg/Desktop/Betty/dataset/dataset_scaled.csv")
    df_labels.to_csv("/Users/sg/Desktop/Betty/dataset/target.csv")

    return df_features, df_scaled


def predict(url=None):
    # Non sscaled dataset
    dataset = "/Users/sg/Desktop/Betty/dataset/dataset.csv"
    df = pd.read_csv(dataset)
    df.drop(df.columns[[0]], axis=1, inplace=True)
    X = df.to_numpy()
    scaler = StandardScaler()
    scaler.fit(X)

    # url_maliciou = http://boasecg7.beget.tech/cgi-bin/index/pcg/free/frebox158418/freemobs/
    # url_benign = https://www.wikipedia.org
    # https://www.youtube.com

    weights_preious_best = [
        -0.1122490849062153,
        0.1905463668530713,
        -0.09342500043429329,
        0.09443263901745655,
        0.3045265656255479,
        -0.18859631001565957,
        0.03200362092638095,
        -0.10903752725349458,
        0.039521007421911954,
        -0.028091465317206653,
        0.049034019587791945,
        0.11872081497106858,
        0.053623336383339056,
        -0.3220738131648578,
        0.05933217547111023,
    ]

    weights = [
        -0.11816955347403929,
        0.26242730456355473,
        -0.12352326101056495,
        0.036362795085118034,
        0.2962844669136361,
        -0.1729564816681796,
        0.03051621579548723,
        -0.14110084433612255,
        0.006062647463853615,
        -0.08915955039190128,
        0.04197603960929685,
        0.11560792963126261,
        0.308296021052551,
        -0.350371296960381,
        0.07022244179636297,
        0.17675280228395482,
        0.11358463502496466,
        -0.18361365111624522,
    ]
    url = input("Enter url: ")

    features = [extract_features(url)]
    features_scaled = scaler.transform(features)
    features_scaled = features_scaled[0]
    print(features_scaled)

    f = 0.0
    for x, w in zip(features_scaled, weights):
        f += x * w
    print(f)
    return "malicious" if f > 0 else "benign"


if __name__ == "__main__":
    # Prepare dataset if was had not already been prepared

    # data_dir = '/Users/sg/Desktop/Betty/dataset/uscx_dataset.csv'

    # # uscx data combine with other data
    # data_uscx = '/Users/sg/Desktop/Betty/dataset/combined.csv'

    # # generaates a scaled statset (dataset_scaled.csv)
    # df, df_scaled = read_data(data_uscx)

    # Pefrorfm prediction

    print(predict())
