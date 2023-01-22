package src;


import javax.xml.soap.*;


public class TestClient {
	
	
	public static void main(String[] args) throws Exception {
        // Create the connection
        SOAPConnectionFactory soapConnectionFactory = SOAPConnectionFactory.newInstance();
        SOAPConnection soapConnection = soapConnectionFactory.createConnection();

        // Send SOAP Message to SOAP Server
        String url = "http://localhost:8081/WebServiceSOAP/services/Client";
        SOAPMessage soapResponseAR = soapConnection.call(createSOAPRequestSearchAllerRetour(), url);
        SOAPMessage soapResponseCo = soapConnection.call(createSOAPRequestConnexion(), url);
        
        String responseAR = getSOAPResponseBody(soapResponseAR);
        String responseCo = getSOAPResponseBody(soapResponseCo);
        // Print the SOAP Response
        System.out.print("Response SOAP Message Aller Retour:");
        System.out.println(responseAR);
        
        System.out.print("Response SOAP Connexion:\n");
        System.out.println(responseCo);
        
        soapConnection.close();

	}
	
    private static SOAPMessage createSOAPRequestSearchAllerRetour() throws Exception {
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage soapMessage = messageFactory.createMessage();
        SOAPPart soapPart = soapMessage.getSOAPPart();

        // SOAP Envelope
        SOAPEnvelope envelope = soapPart.getEnvelope();
        envelope.addNamespaceDeclaration("tps", "http://deployment.ws.tps");

        // SOAP Body
        SOAPBody soapBody = envelope.getBody();
        SOAPElement searchAllerRetour = soapBody.addChildElement("searchAllerRetour", "tps");
        SOAPElement gareD = searchAllerRetour.addChildElement("gareD");
        gareD.addTextNode("paris");
        SOAPElement gareA = searchAllerRetour.addChildElement("gareA");
        gareA.addTextNode("marseille");
        SOAPElement dateD = searchAllerRetour.addChildElement("dateD");
        dateD.addTextNode("2022-10-05_10:00:00");
        SOAPElement dateR = searchAllerRetour.addChildElement("dateR");
        dateR.addTextNode("2022-10-05_15:00:00");
        SOAPElement classe = searchAllerRetour.addChildElement("classe");
        classe.addTextNode("Standard");

        soapMessage.saveChanges();

        return soapMessage;
    }
    
    private static SOAPMessage createSOAPRequestConnexion() throws Exception {
        MessageFactory messageFactory = MessageFactory.newInstance();
        SOAPMessage soapMessage = messageFactory.createMessage();
        SOAPPart soapPart = soapMessage.getSOAPPart();

        // SOAP Envelope
        SOAPEnvelope envelope = soapPart.getEnvelope();
        envelope.addNamespaceDeclaration("tps", "http://deployment.ws.tps");

        // SOAP Body
        SOAPBody soapBody = envelope.getBody();
        SOAPElement searchAllerRetour = soapBody.addChildElement("connexion", "tps");
        SOAPElement mail = searchAllerRetour.addChildElement("mail");
        mail.addTextNode("a");
        SOAPElement mdp = searchAllerRetour.addChildElement("mdp");
        mdp.addTextNode("a");

        soapMessage.saveChanges();

        return soapMessage;
    }
    
    private static String getSOAPResponseBody(SOAPMessage soapResponse) throws Exception {
        SOAPBody body = soapResponse.getSOAPBody();
        return body.getTextContent();
    }
}