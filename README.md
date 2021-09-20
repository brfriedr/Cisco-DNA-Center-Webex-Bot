# Cisco DNA Center Bot

DNA Center is a complete managment and control platform that simpliefies and streamlines network operations. This single, extensible software platform includes intergrated tools for NetOps, SecOps, DevOps and IoT connecvitity with AI/ML technology integrated throughout. 

#### Benefits

* **Simplify Management.** Operate your local and branch networks over a centralized dashboard.
* **Increase Security.** Translate business intent into zero-trust policies and dynamic segmentation of endpoints based on usage behavior.
* **Lower Costs.** Policy-driven provisioning and guided remediation increase network uptime and reduce time spent managing network operations.
* **Transform your network.** Deploy cloud services and applications that benefit from the intelligent network optimization delivered by Cisco DNA Center.
* **Ensure network and application performance:** AI/ML network insights reduce time spent managing network operations and improve user experience.
* **Facilitate offsite IT teams:** Optimized for remote access, a clean, organized dashboard with single-button workflows makes remote management easy.

Webex Teams Bots gives users access to outside services right from their Webex spaces. Bots help users automate tasks, bring external content into the discussions, and gain efficiences. Bots come in all different shapes and sizes such as notifiers, controllers, and assists. 

The ability to intergrate Cisco DNA Center Platform API's into Webex Bots provides us a powerful way to manage and get insites into whats happen within our network. 

# What are we going to do? 

We are going to create a Webex Bot that uses the DNA Center API's to do the following tasks. 

* List Devices 
* Show Device Configuration 
* Show Image Compliance
* Alerting For Assurance Issues 

# Prerequisites 

If you don't already have a [Webex Teams](https://www.webex.com/team-collaboration.html) account, go ahead and register for one. They are free! 

1. You'll need to start by adding your bot to the Webex Teams webiste 
    
    [https://developer.webex.com/my-apps](https://developer.webex.com/my-apps)
    
2. Click **Create a New App** 
    
    ![Screen Shot 2021-09-17 at 11 01 15 AM](https://user-images.githubusercontent.com/80418373/133818934-1b084325-8d37-471c-82f6-0e23971794d0.png)
    
3. Click **Create a Bot**
    
    ![Screen Shot 2021-09-17 at 11 02 41 AM](https://user-images.githubusercontent.com/80418373/133819125-0e231885-99b0-4708-b021-28fc2878bd06.png)
    
4. Fill out all the details about your bot. 
    
    ![Screen Shot 2021-09-17 at 11 04 27 AM](https://user-images.githubusercontent.com/80418373/133819329-9f9d1bf4-76ed-4c25-960b-d2d2ef524e61.png)
    
5. Click **Add Bot**

6. On the Congratluations screen, make sure to copy the Bot's Access token, you will need this. 

# ngrok 

[ngrok](https://ngrok.com/) makes it easy for you to develop your code with a live bot. 

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
3. You will use the Forwarding ULR in the config.py file with this URL: 

        TEAMS_BOT_URL=os.envrion.get('TEAMS_BOT_URL','http://this.is.the.url.you.net.ngrok.io')
        
# Config File 

Update the config.py file with the releveant information of your Cisco DNA Center Appliance or you can use our DNA Center Sandbox.

Example config.py with Cisco DNA Center Sandbox information: 

        import os
        DNAC=os.environ.get('DNAC','https://sandboxdnac.cisco.com')
        DNAC_PORT=os.environ.get('DNAC_PORT',443)
        DNAC_USER=os.environ.get('DNAC_USER','devnetuser')
        DNAC_PASSWORD=os.environ.get('DNAC_PASSWORD','Cisco123!')
        WEBEX_BOT_ACCESS_TOKEN=os.environ.get('WEBEX_BOT_ACCESS_TOKEN','Enter your webex toekn from the preq step 6')
        TEAMS_BOT_URL=os.envrion.get('TEAMS_BOT_URL','http://this.is.the.url.you.net.ngrok.io')




 



