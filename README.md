# Cloud9 Environment For Online Processing of TozStore Data

This Repository includes instructions for easily setting up a cloud based command line environment/unix console and IDE 
to process large files that are securely stored using TozStore. This document is designed to be usable for people that 
have never interacted with Amazon AWS previously. In many cases the official documentation will be linked too, and then 
screen shots will be included as additional support.
 
Upon following all of the steps, you will have an AWS account containing an [AWS Cloud9](https://aws.amazon.com/cloud9/) 
instance, a cloud based integrated development environment. The Cloud9 instance will contain python scripts to help download 
large files from TozStore, move them to an [AWS S3](https://aws.amazon.com/s3/) bucket on your AWS account and store meta
 data in an [AWS RDS](https://aws.amazon.com/rds/) database running [Postgresql 10](https://www.postgresql.org/), which is also
 hosted on your account.
 
**Things you will need**
 * An E3DB client (If you are part of an institution you may have been provided one, otherwise a new one can be created
  at [Tozny.com](https://tozny.com))
  * A form of payment for an AWS account, as of February 2019 all of the default values for this project fell into the 
  AWS Free tier for new customers.

 
 ## Setting up an Amazon AWS Root Account
 
 The first step is to create a new Amazon AWS Account.
 
 Begin by going to the [AWS Home page](https://aws.amazon.com/) and click on the `Signup` button in the upper right hand 
 corner. You should now be on a page that resembles
 
 ![SignupPage](readme-images/AWS-Signup.png)
 
 Fill out this page and press continue (as always it is highly recommended to use a new secure password, as this
  account will be linked to a credit card).
 Continue through the rest of the signup flow, including entering a credit card 
 and verifying your identity. Additional instructions are available
  [here](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/).
  
  
  
 On the *Support Plan*  page you can select no support plan needed, it is not needed for this setup.
 
 ![Support Plan](readme-images/AWS-support-plan.png)
 
 Once completed click on *Sign in to the Console*
 
 ![Sign-in to console](readme-images/aws-signin.png)
 
 Enter the email address and password that you created during the signup flow and you are in!
 
  ***This is the time to remind you, if you haven't already, to secure your root account password somewhere safe. We recommend 
 [1Password](https://1password.com/), alternatively [Lastpass](https://www.lastpass.com/) is also another option.***
 
 ***Enabling Multi-Factor Authentication (MFA, 2FA) for this account is also recommended, instructions are available 
 [here](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html#enable-virt-mfa-for-root)***
 
 ## Creating an administrative user
 
 To follow [AWS best practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_root-user.html#id_root-user_manage_mfa)
 , the next step is to create a new IAM user with full permissions that is not the root account.
 
 ### Steps
 
 1. Allow IAM users access to the billing dashboard. The instructions can be found here, 
 [AWS Instructions](https://docs.aws.amazon.com/awsaccountbilling/latest/aboutv2/grantaccess.html).
    1. Click on your account name in the upper right corner (example-account in the screenshot) and then `My Account`. 
    you should now be on a page with `Account Settings ` and `Contact Information` sections (and others)
    
        ![My-Account](readme-images/my-account.png)
    
    1. You should now be on a page with `Account Settings ` and `Contact Information` sections (and others). While at 
    the top copy down the Account Id (it is a twelve digit number that you will need later)
    
        ![Account-Id](readme-images/aws-account-id.png)
        
    1. Halfway down the page should be a section called `IAM User and Role Access to Billing`, depending on your screen 
    size, some of that may be truncated. To the right side of that is an `edit` button, click that.
    
        ![IAM user billing](readme-images/iam-billing.png)
    1. Select the `Activate IAM Access` checkbox that is now visible and press update. Once clicked that checkbox should
    disappear and a message saying "*IAM user/role access to billing information is activated.*" should be visible
    
    1. Return to the main console page by clicking on the `AWS` logo in the top left corner of the page
    
        ![aws-logo](readme-images/aws-logo.png)
1. From the Main page click on `Services` to open the service selector.

    ![aws-service](readme-images/aws-services.png)

1. In the upper right corner of the page between the account name and `Support` will be the name of a geographic phrase, such
as `Ohio`, `Oregon`, or `US West`.  Click on that to open the region selector. **For later stages of this tutorial you 
must select `US West (Oregon)`.** You will now see that the browser url has become `us-west-2.console.aws`, 
and the location selector will now say `Oregon`

    ![location-selector](readme-images/location-selector.png)
    
    ![us-west-2](readme-images/us-west-selected.png)

1. Listed in the `Management & Governance` sections is `CloudFormation` click that. (Alternatively in the find a service 
text field, begin typing `CloudFormation` and the result that appears can be clicked on).

    ![cloud-formation](readme-images/cloud-formation.gif)
1. On this page there should be a button that says `Create new stack`. Click that ***Note there are 2 different cloud 
formation UIs at the moment, one for root users and one for IAM Users, if the screenshots don't look right in this 
section the ones in the next section may be a better visual representation, but the text is very similar***

    ![new-stack-user](readme-images/create-new-stack-user.png)
1. On the next page select the `Specify an Amazon S3 template URL` and paste in.
    
    `https://s3.us-west-2.amazonaws.com/tozny-fedramp-cloudformation/v1/cloud-formation-user.json`
    
    and then press next. A copy of that CloudFormation file also lives in this repository at 
    [user-cloud-formation](cloudformation/cloud-formation-user.json) for reference
1. The next page has **3** parameters that need to be filled out. Once filled press next.
    1. Stack name: This can be anything you like, but descriptive. Something like `administrative-user-creation` is a 
    good choice.
    1. UserName: this is the username that you will use to log in with, I like first initial last name (this value must be 3-41 characters).
    1. UserPassword: this is the password to log in with that user. Notice that this password is only entered once so
    make sure it is correctly entered. This account will be able to spend money so make sure the password is unique and strong
    both password managers mentioned previously can automatically generate a strong password for you.
1. On the next page scroll to the bottom and press next again
1. You are now on the `Review` page. Scroll to the bottom. You will see a blue alert. Activate the I acknowledge check 
    mark and then press create.
    
    ![create-user-stack](readme-images/create-user-stack-check-mark.png)

1. This is the stack creation page, you will see that the stack creation process is in progress. This process should 
not take more than a minute or two. If you refresh the page it will change to `CREATE_COMPLETE`
    
    **Before**
    
    ![in-progress-user](readme-images/create-user-in-progress.png)
    
    **After**
    
    ![create-complete-user](readme-images/create-user-complete.png)
    
 1. After this new user has been created, log out of the root user account. (Make sure you have the account id, you will 
 need it to login as the new user)
 
 
 ## Logging in as the New IAM User
 
 Now that your new IAM user has been created you can log in as that user
 
 1. From the main [AWS Page](https://aws.amazon.com/) hover over `My Account`, and then click `AWS Management Console`. This will
 bring you to the root user account login page.
 1. Press the `Sign in to a different account` link
 1. On that next form enter your 12 digit account number that was written down in the last section and press `next`
 1. On the next page the account id should be prefilled, and match what was just entered. Then enter the username and password of the newly created user and press `Sign In`
 1. You are now logged in and should see in the upper right corner `<Your-user-name@your-account-id>`
    
    ![sign-in-flow](readme-images/login.gif)
   
 1. It is recommended at this time that you setup MFA for this account as well. 
 [AWS Instructions](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_mfa_enable_virtual.html#enable-virt-mfa-for-iam-user)
    1. From the services dropdown select `IAM` from the `Security, Identity & Compliance` section, or you can search 
    for `IAM` and select it.
    1. In the `IAM Resources` Section click `Users: 1` (This number could potentially be different but should be 1 at 
    this point if only one IAM user has been created).
    
        ![IAM Users](readme-images/go-to-users.png)
    1. Click on the username that you just logged in as.
    
        ![select-user](readme-images/select-user.png)
    1. Click on `Security credentials`
    
        ![security-credentials](readme-images/go-to-security-credentials.png)
    1. Click on `Manage` next to `Assigned MFA Devices
        
        ![manage-mfa](readme-images/manage-mfa.png)
    1. Select the type of MFA you want to use, most people will use a virtual MFA such as Google Authenticator, or 
    [Authy](https://authy.com/). If you have a hardware device (such as a [Yubi-Key](https://www.yubico.com/)) that will work as well.
    1. Follow the instructions on the prompt (For virtual MFA it will look similar to the below screen grab)
    
    ![mfa-registration](readme-images/mfa-registration.png)
    
 If you followed this readme as a way to setup a new AWS account and register a single new administrative user you have 
 completed that and AWS is now yours to explore! The next sections will setup an infrastructure that can download and 
 store large files from TozStore for cloud native secure data processing.
 
 ## Creating an S3, RDS, Cloud9 Stack using CloudFormation
 
We are going to once again use cloud formation to create this stack.

**Make sure that the region has been set to `US-West Oregon` before beginning this process**

1. From the AWS console page you are going to open the `Services` drop down. Then open `CloudFormation`, either from
`Management & Governance` or by searching. *Tip: On the left side of the Services drop down is the history, which lists the
 four most recently visited services*
1. Click `create stack`

    ![create-stack-resource](readme-images/create-stack-resource.png)
1. Under Specify Template, `Template source` select `Amazon S3 URL`, and paste in 

    `https://s3.us-west-2.amazonaws.com/tozny-fedramp-cloudformation/v1/cloud-formation-resources.json`
    
    and click `Next` (sometimes the stack creator buttons take two clicks to go to the next page)
    
    ![specify-template](readme-images/specify-template.png)

1. On the next page fill in a stack name, the example images use `tozstore-cloud9`. The only other value that must be set is
`DBPassword` this is to set the master password for Postgres database that will be created. As always this should be a strong password.
This password is not easy to recover and should be stored in a safe place, like a password manager.

    The other fields can be left as is. If the default parameters do not suit your needs, other options for cloud9 are 
    [here](https://aws.amazon.com/ec2/instance-types/) and other RDS options are [here](https://aws.amazon.com/rds/instance-types/).
    *Note: Other options may not fall in the free tier and some options are very expensive*
    
    ![resource-parameters](readme-images/stack-details.png)
    
    click next
1. The next page is to configure options, in this case no additional configuration is needed, scroll to the bottom and press next
1. On the review page scroll down to the bottom and press `Create stack`

    ![stack-recording](readme-images/create-stack-recording.gif)
1. This will bring you to the events page for the stack. The building of this stack will take 10-30 minutes
1. After some time on the main CloudFormation page you should see a list of two new stacks 
(if following this tutorial on a new AWS account, there should be three total stacks). The stack you named in a previous step and
an `aws-cloud9...` stack, this is a sub stack that was created by the main stack.
    
    ![completed-stacks](readme-images/complete-stacks.png)
    
The infrastructure is now setup, all that is left is bootstrapping and configuration

### Pieces of information you will need for the next step

1. Now that the stack is built, click on the main stack, in the images this is called `tozstore-cloud9`.
1. On this page there is an `outputs` tab, click on that

    ![outputs-tab](readme-images/outputs-tab.png)
1. On the output page there should be two rows with keys, `S3Bucket` and `Ta2DB`. Record both of the values, for the next step

## Bootstrapping

1. Open up the `Services` drop down and select `Cloud9` from under `Developer Tools`, as always you can find this by
typing in the search field as well.

1. On this page you should see an environment names `TA2 Cloud9 Instance`, go ahead and click `Open IDE`

    ![cloud9-instance-list](readme-images/cloud9-instances.png)

1. It may take a minute to load and then you will see something like this

    ![cloud9-fresh](readme-images/cloud9-fresh.png)
    
1. You need to clone the git repository this README is in into the cloud 9 instance to do that type
 `git clone https://github.com/tozny/cloud9-integration-work.git`into the terminal at the bottom
    ![terminal](readme-images/terminal.png)
 
1. There will now be a new folder on the left hand side called `cloud9-integration-work`

1. type `cd cloud9-integration-work`

1. Now there is some configuration that needs to be done
    1. In the `cloud9-integration-work` directory is  a file called `flyway.conf`, there are two fields in this file that
    need to be updated
        1. The DB endpoint recorded in a previous section replaces `<DB_HOST_HERE>`
        1. The DB password entered during stack creation replaces `<DB PASSWORD HERE>`
        1. Save file
    1. If you open the directory `ta2resources`, inside `cloud9-integration-work` there is a file called `config.json`.
    Double click it and it will open in the editor. There are 4 fields that need to be filled in. 
        1. Your Tozstore client credentials, There needs to be a one set of brackets around the keys.
        1. The S3 Bucket name recorded in a previous section replaces `<BUCKET NAME HERE>`
        1. The DB endpoint recorded in a previous section replaces `<DB_HOST_HERE>`
        1. The DB password entered during stack creation replaces `<DB PASSWORD HERE>`
        1. Save file
    1. The Default python interpreter must be updated to Python3
        1. Select the `AWS Cloud9` and click `Preferences`.
        1. Click on `Python Support`
        1. Select the dropdown that says `Python 2` and select `Python 3`. You may close the preferences tab
            ![preferences](readme-images/preferences.png)
1. A few tools need to be installed.
    1. type `cd ~/environment/cloud9-integration-work`
    1. type `make setup`
        1. There may be a few time where it pauses and asks if you are sure you want to install the files. type `Y` and then
        press return

## Downloading data

This environment is now all setup and ready to go.  You can close the Cloud9 instance and reopen it by clicking `launch ide`.
If the environment is closed for an extended period of time (by default configured to 30 minutes) the instance will shut down,
all this means is that the next time you launch the instance it will take a little while longer. But it will come back just the way you left it

1. Open up the Cloud9 Instance
1. Type `cd ~/environment/cloud9-integration-work`
1. On the left tray open `cloud9-integrationwork/ta2resources/working-script.py`
1. For the simplest implementation with `working-script.py` all you need to do is click the `Run` button at the top of the interface.
This will download the first 50 records that the client has permissions to read with the specified record type. 
If there are more than 50 records it will prompt to see if more files should be collected. Once all files fitting the 
search have been collected the display will prompt if you want to download this will also list the total number of 
records and total size to be downloaded. Follow the onscreen prompts to complete
1. Once completed the files will be stored in your S3 Bucket and metadata related to the the files can be found in the Postgres Database

### Advanced searching

The search system is backed by an elastic search like system, that can run a very broad type of search queries. For full
 class documentation see [here](https://github.com/tozny/e3db-python/blob/master/e3db/types/search.py#L189) and for some
 simple examples see [here](https://github.com/tozny/e3db-python/blob/master/README.md)


#### Search Examples
    
Todo

### Post-download Processing

The S3 bucket holds all of the downloaded files. You can access the bucket in the console by opening the `Services` drop 
down and searching for `S3`, it can also be found under the `Storage` section. On that page will be a bucket with the 
name recorded from the outputs. By clicking in you can see all of the objects listed.

Metadata for the files in the s3 bucket, can be found in the RDS instance that was created. It can be accessed using the 
[PSQL](http://postgresguide.com/utilities/psql.html) tool. It can be started with the command

`psql -h <DB_HOST_HERE> -U ta2_user -d ta2db` you will be prompted for the db password, paste it in and press return.

The database schema can be found [here](migrations/V1__record_storage.sql). Don't forget that the user you are logging in with
has full read, write permissions, so be careful not to delete any data if you are not precisely sure of the outcome.

The [Flyway command line tool](https://flywaydb.org/) was used to do the migrations, and can be used again if more migrations
are desired
        
    
