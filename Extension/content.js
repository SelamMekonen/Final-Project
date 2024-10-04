var testdata;
var prediction;

function predict(data,weight){
    var f = 0;
    weight = [-0.11825775, 0.2624012, -0.123544, 0.03668607, 0.29645486, -0.17309506,
        0.03067645, -0.14074015, 0.00454814, -0.08927203, 0.04223589, 0.11251733,
        0.29587528, -0.35029427, 0.09538272, 0.1786489, 0.115073, -0.18356105]
      ;
    for(var j=0;j<data.length;j++) {
      f += data[j] * weight[j];
    }
    return f > 0 ? 1 : -1;
}

function entropy(str) {
    const unique_chars = new Set(str);
    let entropy = 0;
    
    for (let char of unique_chars) {
      if (/[a-zA-Z]/.test(char)) {
        const p_i = parseFloat(str.match(new RegExp(char, 'g')).length) / str.length;
        entropy -= p_i * Math.log10(p_i);
      }
    }
    
    return entropy;
  }


function getCharacterContinuityRate(domain) {
    let longestLetterToken = 0;
    let longestDigitToken = 0;
    let longestSymbolToken = 0;
  
    let countLetter = 0;
    let countDigit = 0;
    let countSymbol = 0;
  
    for (let i = 0; i < domain.length; i++) {
      const c = domain.charAt(i);
  
      if (/[a-zA-Z]/.test(c)) {
        countLetter++;
        countDigit = 0;
        countSymbol = 0;
        if (countLetter > longestLetterToken) {
          longestLetterToken = countLetter;
        }
      } else if (/\d/.test(c)) {
        countDigit++;
        countLetter = 0;
        countSymbol = 0;
        if (countDigit > longestDigitToken) {
          longestDigitToken = countDigit;
        }
      } else {
        countSymbol++;
        countDigit = 0;
        countLetter = 0;
        if (countSymbol > longestSymbolToken) {
          longestSymbolToken = countSymbol;
        }
      }
    }
  
    const charContinuityRate =
      (longestDigitToken + longestLetterToken + longestSymbolToken) / domain.length;
  
    return charContinuityRate;
  }


function getNumberRateUrl(url) {
    const urlParts = url.split("/");
  
    let countDigits = 0;
    for (let i = 0; i < urlParts.length; i++) {
      countDigits += Array.from(urlParts[i]).reduce(
        (count, char) => count + /\d/.test(char),
        0
      );
    }
  
    return countDigits / url.length;
  }

 
function getNumberRateAfterPath(url) {
    const afterPathStr = url.split("/").pop(); // Last element in the splitup url
    if (!afterPathStr) {
      return -1;
    }
  
    const countDigitsAfterPathStr = Array.from(afterPathStr).reduce(
      (count, char) => count + /\d/.test(char),
      0
    );
  
    return countDigitsAfterPathStr / afterPathStr.length;
  }
  
  function getAvgPathtokenLen(parsedUrl) {
    const pathTokensList = parsedUrl.pathname.split("/");
  
    if (!pathTokensList.length) {
      return 0;
    }
  
    const totalLengthOfTokensInPathList = pathTokensList.reduce(
      (sum, token) => sum + token.length,
      0
    );
  
    const avgTokenLengthInPathList =
      totalLengthOfTokensInPathList / pathTokensList.length;
  
    return avgTokenLengthInPathList;
  }

function isIPInURL(url){
    var reg =/\d{1,3}[\.]{1}\d{1,3}[\.]{1}\d{1,3}[\.]{1}\d{1,3}/;
    if(reg.exec(url)==null){
        console.log("NP");
        return -1;
    }
    else{
        console.log("P");
        return 1;
    }
}

function isLongURL(url){   
    if(url.length<54){
        console.log("NP");
        return -1;
    } 
    else if(url.length>=54 && url.length<=75){
        console.log("Maybe");
        return 0;
    }
    else{
        console.log("P");
        return 1;
    }
  }


  function isTinyURL(url){    
    if(url.length>20){
        console.log("NP");
        return -1;
    } 
    else{
        console.log("P");
        return 1;
    }
  }


function isAlphaNumericURL(url) {
    let search = "@";
    if (!url.includes(search)) {
      return -1;
    } else {
      return 1;
    }
  }

function isRedirectingURL(url){
    var reg1 = /^http:/
    var reg2 = /^https:/
    var srch ="//";
    if(url.search(srch)==5 && reg1.exec(url)!=null && (url.substring(7)).match(srch)==null){
        console.log("NP");
        return -1;
    }
    else if(url.search(srch)==6 && reg2.exec(url)!=null && (url.substring(8)).match(srch)==null){
        console.log("NP");
        return -1;
    }
    else{
        console.log("P");
        return 1;
    }
  }
  
  
function prefix_suffix(domain) {
    var match = domain.match("-");
    return match ? -1 : 1;
  }

  

function isIllegalHttpsURL(url) {
    const srch1 = "//";
    const srch2 = "https";
    
    if (url.includes(srch1) && !url.includes(srch2, url.indexOf(srch1))) {
        return -1;
    } else {
        return 1;
    }
  }


function double_slash_redirecting(url) {
    const last_double_slash = url.lastIndexOf("//");
    return last_double_slash > 6 ? -1 : 1;
  }
  

function https_token(url) {
    const http_https = new RegExp("^http[s]?", "i");
    let match = url.match(http_https);
    if (match && match.index === 0) {
      url = url.slice(match[0].length);
    }
    match = url.match(/http|https/i);
    return match ? -1 : 1;
  }


function having_sub_domain(url) {
    if (isIPInURL(url) == -1) {
        const re = new RegExp(
            "(([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\.([01]?\\d\\d?|2[0-4]\\d|25[0-5])\\."
            + "([01]?\\d\\d?|2[0-4]\\d|25[0-5]))|(?:[a-fA-F0-9]{1,4}:){7}[a-fA-F0-9]{1,4}"
        );
        const match = url.match(re);
        const pos = match ? match.index + match[0].length: -1;
        url = url.slice(pos);
    }
    const num_dots = [...url.matchAll(/\./g)].map(m => m.index);
    if (num_dots.length <= 3) {
        return 1;
    } else if (num_dots.length == 4) {
        return 0;
    } else {
        return -1;
    }
  }

function main() {
    
    var url = window.location.href; 
    
    
    
    var domain = new URL(url).hostname;


    var parsedUrl = new URL(url);
    // const domain = parsedUrl.hostname.split('.');

    var path = parsedUrl.pathname;
    var args = parsedUrl.search;

    var filename = parsedUrl.pathname.split('/').pop();

    var Entropy_Domain = entropy(domain);
    var CharacterContinuityRate = getCharacterContinuityRate(domain)
    var numberRateFileName = filename ? (filename.match(/\d/g) || []).length / filename.length : -1;
    var domainUrlRatio = domain.length / url.length;
    var NumberRate_URL = getNumberRateUrl(url)
    var PathDomainRatio = path.length / domain.length;
    var NumberRate_AfterPath = getNumberRateAfterPath(url)
    var avgpathtokenlen = getAvgPathtokenLen(parsedUrl)
    var is_ip_exist = isIPInURL(url)
    var is_long = isLongURL(url)
    var is_tiny = isTinyURL(url)
    var is_alphanumeric = isAlphaNumericURL(url)
    var is_redirecting = isRedirectingURL(url)
    var is_hyphen_domain = prefix_suffix(domain)
    var double_slash = double_slash_redirecting(url)
    var http_in_domain = https_token(url)
    var sub_domain = having_sub_domain(url)
    var isIllegalHttps = isIllegalHttpsURL(url)



    testdata = [
    Entropy_Domain, CharacterContinuityRate,
    numberRateFileName, domainUrlRatio, NumberRate_URL, 
    PathDomainRatio, NumberRate_AfterPath, avgpathtokenlen, 
    is_ip_exist, is_long, is_tiny, is_alphanumeric, is_redirecting,
    is_hyphen_domain, double_slash, http_in_domain, sub_domain,
    isIllegalHttps]

    console.log(testdata)
    
    

    }

main()

prediction = predict(testdata);

chrome.extension.sendRequest(prediction);


