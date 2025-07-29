from burp import IBurpExtender, IHttpListener, IRequestInfo

class BurpExtender(IBurpExtender, IHttpListener):

    def registerExtenderCallbacks(self, callbacks):
        self._callbacks = callbacks
        self._helpers = callbacks.getHelpers()
        callbacks.setExtensionName("Zs_sd_security_test: 7965735f62795f706173735f73645f7365637572697479")
        callbacks.registerHttpListener(self)
        print("Zs_sd_security_test: 7965735f62795f706173735f73645f7365637572697479")

    def processHttpMessage(self, toolFlag, messageIsRequest, messageInfo):
        if messageIsRequest:
            request = messageInfo.getRequest()
            analyzedRequest = self._helpers.analyzeRequest(request)

            headers = list(analyzedRequest.getHeaders())

            # Add your custom header here
            header_to_add = "X-My-Custom-Header: MyValue"

            # Check if header already present
            header_names = [h.split(":")[0].strip().lower() for h in headers]
            if header_to_add.split(":")[0].lower() not in header_names:
                headers.append(header_to_add)

                body = request[analyzedRequest.getBodyOffset():]
                newRequest = self._helpers.buildHttpMessage(headers, body)
                messageInfo.setRequest(newRequest)
