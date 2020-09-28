// Check Token API
// DataTeam
// 



exports.handler =  function(event, context, callback) {
    
    
    
    var AWS = require('aws-sdk'),
        region = "us-east-1",
        secretName = "api/token",
        secret,
        decodedBinarySecret;
    
    
    var client = new AWS.SecretsManager({
        region: region
    });
    
    
    var retorno_token = client.getSecretValue({SecretId: secretName}, function(err, data) {
        if (err) {
            console.log(err);
        }
        
        else {
            if ('SecretString' in data) {
                secret = data.SecretString;
            } else {
                let buff = new Buffer(data.SecretBinary, 'base64');
                decodedBinarySecret = buff.toString('ascii');
            }
        }
        
        
        let exported_secret = JSON.parse(secret);
        exported_secret = exported_secret.secret_token;
        
   
        
        var token = event.authorizationToken;
        switch (token) {
        case exported_secret:
            callback(null, generatePolicy('user', 'Allow', event.methodArn));
            break;
        case 'deny':
            callback(null, generatePolicy('user', 'Deny', event.methodArn));
            break;
        case 'unauthorized':
            callback("Unauthorized");   // Return a 401 Unauthorized response
            break;
        default:
            callback("Error: Invalid token"); // Return a 500 Invalid token response
    }
        
        
    });
  
    

    
    
    
    
};

// Help function to generate an IAM policy
var generatePolicy = function(principalId, effect, resource) {
    var authResponse = {};
    
    authResponse.principalId = principalId;
    if (effect && resource) {
        var policyDocument = {};
        policyDocument.Version = '2012-10-17'; 
        policyDocument.Statement = [];
        var statementOne = {};
        statementOne.Action = 'execute-api:Invoke'; 
        statementOne.Effect = effect;
        statementOne.Resource = resource;
        policyDocument.Statement[0] = statementOne;
        authResponse.policyDocument = policyDocument;
    }
    
    // Optional output with custom properties of the String, Number or Boolean type.
    authResponse.context = {
        "stringKey": "stringval",
        "numberKey": 123,
        "booleanKey": true
    };
    return authResponse;
}





