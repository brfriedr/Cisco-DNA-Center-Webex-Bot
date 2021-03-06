# Cisco DNA Center Bot

DNA Center is a complete management and control platform that simplifies and streamlines network operations. This single, extensible software platform includes integrated tools for NetOps, SecOps, DevOps and IoT connectivity with AI/ML technology integrated throughout. 

#### Benefits

* **Simplify Management.** Operate your local and branch networks over a centralized dashboard.
* **Increase Security.** Translate business intent into zero-trust policies and dynamic segmentation of endpoints based on usage behavior.
* **Lower Costs.** Policy-driven provisioning and guided remediation increase network uptime and reduce time spent managing network operations.
* **Transform your network.** Deploy cloud services and applications that benefit from the intelligent network optimization delivered by Cisco DNA Center.
* **Ensure network and application performance:** AI/ML network insights reduce time spent managing network operations and improve user experience.
* **Facilitate offsite IT teams:** Optimized for remote access, a clean, organized dashboard with single-button workflows makes remote management easy.

Webex Teams Bots gives users access to outside services right from their Webex spaces. Bots help users automate tasks, bring external content into the discussions, and gain efficiencies. Bots come in all different shapes and sizes such as notifiers, controllers, and assists. 

The ability to integrate Cisco DNA Center Platform API's into Webex Bots provides us a powerful way to manage and get insights into whats happing within our network. 

# What are we going to do? 

We are going to create a Webex Bot that uses the DNA Center API's to do the following tasks. 

* List Devices 
* Show Device Configuration 
* Show Image Compliance
* Alerting For Assurance Issues 

# Prerequisites 

If you don't already have a [Webex Teams](https://www.webex.com/team-collaboration.html) account, go ahead and register for one. They are free! 

1. You'll need to start by adding your bot to the Webex Teams website 
    
    [https://developer.webex.com/my-apps](https://developer.webex.com/my-apps)
    
2. Click **Create a New App** 
    
    ![Screen Shot 2021-09-17 at 11 01 15 AM](https://user-images.githubusercontent.com/80418373/133818934-1b084325-8d37-471c-82f6-0e23971794d0.png)
    
3. Click **Create a Bot**
    
    ![Screen Shot 2021-09-17 at 11 02 41 AM](https://user-images.githubusercontent.com/80418373/133819125-0e231885-99b0-4708-b021-28fc2878bd06.png)
    
4. Fill out all the details about your bot. 
    
    ![Screen Shot 2021-09-17 at 11 04 27 AM](https://user-images.githubusercontent.com/80418373/133819329-9f9d1bf4-76ed-4c25-960b-d2d2ef524e61.png)
    
5. Click **Add Bot**

6. On the Congratulations screen, make sure to copy the Bot's Access token, you will need this. 

# ngrok 

[ngrok](https://ngrok.com/) makes it easy for you to develop your code with a live bot. Ngrok exposes local servers behind NATs and firewalls to the public internet over secure tunnels. It instantly creates a public HTTPS url for a webist running locacally on your development machine. Ngrok offloads TLS, so you don't have to worry about your configuration. 

You can find installation instructions here: https://ngrok.com/download

1. After you've installed ngrok, in another window start the service 
    
        ngrok http 8080

2. You should see screen that looks like this: 

        ngrok by @inconshreveable                                                     (Ctrl+C to quit)

        Session Status                online
        Account                       brandon.friedrich@gmail.com (Plan: Free)
        Version                       2.3.40
        Region                        United States (us)
        Web Interface                 http://127.0.0.1:4040
        Forwarding                    http://this.is.the.url.you.net.ngrok.io -> http://localhost:8080
        Forwarding                    http://this.is.the.url.you.net.ngrok.io -> http://localhost:8080

        Connections                   ttl     opn     rt1     rt5     p50     p90
                                        0       0       0.00    0.00    0.00    0.00
3. You will use the Forwarding URL in the config.py file with this URL: 

        TEAMS_BOT_URL=os.envrion.get('TEAMS_BOT_URL','http://this.is.the.url.you.net.ngrok.io')
        
# Config File 

Update the config.py file with the relevant information of your Cisco DNA Center Appliance or you can use our DNA Center Sandbox.

Example config.py with Cisco DNA Center Sandbox information: 

        import os
        DNAC=os.environ.get('DNAC','https://sandboxdnac.cisco.com')
        DNAC_PORT=os.environ.get('DNAC_PORT',443)
        DNAC_USER=os.environ.get('DNAC_USER','devnetuser')
        DNAC_PASSWORD=os.environ.get('DNAC_PASSWORD','Cisco123!')
        WEBEX_BOT_ACCESS_TOKEN=os.environ.get('WEBEX_BOT_ACCESS_TOKEN','Enter your webex toekn from the preq step 6')
        TEAMS_BOT_URL=os.envrion.get('TEAMS_BOT_URL','http://this.is.the.url.you.net.ngrok.io')

# Webex Bot Script 

The Bot.py script is leveraging the Flask web service [micro-framework](http://flask.pocoo.org/). We are using ngrok to be used to tunnel traffic back to your local machine sites. When interacting with the Bot, we are calling functions in the DNAC.py script to make API calls to the Cisco DNA Center you specified in the config file. 

This script is an example of different interactions you could create between your Bot and Cisco DNA Center. 

Below are the example interactions with the Bot Script. 

    Help me - I will display what I can do.
    Hello - I will display my greeting message.
    List devices - I will list devices in DNA Center.
    Show Device Config - I will attach the device configuraiton for your device.
    Image Compliance - I will show the image software compliance.

Update the config.py parameters then run the Bot.py script to see it in action! 

Example output

![Screen Shot 2021-09-20 at 3 05 42 PM](https://user-images.githubusercontent.com/80418373/134067914-ed1add42-0d41-4fc6-a50c-7edf187dfa77.png)


# Cisco DNA Center Real Time Event Alerts to Webex Teams Bot 

Cisco DNA Center has a powerful issue correlation engine for wired and wireless networks. Real time feeds of network telemetry is able to identify issues and provide context for resolution. We now have the ability to send those notifications to a Webex Team Rooms in 2.2.3.0 release. 

1.) In Cisco DNA Center navigate to Platform -> Developer Toolkit and the Events Tab.

![Screen Shot 2021-09-20 at 2 55 19 PM](https://user-images.githubusercontent.com/80418373/134066574-61efac9b-fbda-4f51-a5a8-ed001d69fffe.png)

2.) Select the events you want to be notified about to your Webex Teams Room then click "Subscribe". 

3.) Create a Name for the subscription then select Webex for the Subscription Type.  

![Screen Shot 2021-09-20 at 2 57 27 PM](https://user-images.githubusercontent.com/80418373/134066822-27516f03-364c-479a-bd34-11ed13266167.png)

4.) Enter the Webex URL along with the Webex Room ID where you want the alerts to be posted and your Webex Access Bot Token. (You can find your webex room id's at [developer.webex.com](https://developer.webex.com/docs/api/v1/rooms/get-room-meeting-details))

![Screen Shot 2021-09-20 at 3 01 57 PM](https://user-images.githubusercontent.com/80418373/134067388-9e484b6b-55f8-4382-bb36-3f24099df4d6.png)

![Screen Shot 2021-09-20 at 3 01 06 PM](https://user-images.githubusercontent.com/80418373/134067277-7414dac6-9360-4726-ad7d-7626b803b50a.png)

5.) You can now test your integration by selecting "Try it" 

![Screen Shot 2021-09-20 at 3 03 34 PM](https://user-images.githubusercontent.com/80418373/134067606-b322bee0-a765-4578-abfe-73d69e5cd247.png)

6.) If you setup everything correctly you will see the notification in your Cisco Webex Team Room. 

![Screen Shot 2021-09-20 at 3 04 06 PM](https://user-images.githubusercontent.com/80418373/134067679-1caac760-b9ae-41e8-acca-ddfd7b62391e.png)

# Links to DevNet Learning Labs

Here is a link to the Cisco DNA Center Devnet Learning Lab to learn how to leverage the Cisco DNA Center API's.

[Introduction to Cisco DNA Center REST APIs](https://developer.cisco.com/learning/modules/dnac-rest-apis)

# License

This project is licensed to you under the terms of the [Cisco Sample Code License.](https://github.com/brfriedr/Cisco-DNA-Center-Webex-Bot/blob/main/LICENSE)
