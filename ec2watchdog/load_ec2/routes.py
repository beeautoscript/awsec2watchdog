from os import access
from flask import Blueprint,render_template,url_for, flash, redirect, request,jsonify
from ec2watchdog import app,db
from ec2watchdog.models import AccessKey
from ec2watchdog.load_ec2.forms import Ec2SshForm,Ec2FilterForm
import datetime
import boto3
import botocore
from boto3 import client, resources
import datetime
from dateutil.tz import tzutc
import base64
import webbrowser
import time

#Blueprint object
blue = Blueprint('load_ec2',__name__,template_folder='templates')

#Load EC2
@blue.route('/loadec2/<string:rowinfo>',methods=['GET','POST'])
def loadec2(rowinfo):
    instance_id_list = []
    rowid = rowinfo.split(":")[0]
    region = rowinfo.split(":")[1]

    #get access info
    get_access_info = AccessKey.query.get(rowid)
    
    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid
    
    # connect to boto3 ec2
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    try:
        instance_load = client.describe_instances()
        instance_load_length = len(instance_load['Reservations'])
        instance_data = instance_load['Reservations']
        #print(instance_data)
        for i in instance_data:
            instance_id_list.append(i['Instances'][0]['InstanceId'])
        
    except botocore.exceptions.ClientError:
        flash(f'Access Denied to {region}','danger')
        return redirect(url_for('load_ec2.ec2',rowid=rowid))
    return render_template('load_ec2/load_ec2.html',title="Load EC2",instance_data=instance_data,instance_load_length=instance_load_length,row=rowid,awsregion=region,instance_id_list=instance_id_list)

#Filter EC2
@blue.route('/ec2/<int:rowid>',methods=['POST','GET'])
def ec2(rowid):
    form = Ec2FilterForm()
    if form.validate_on_submit():
        return redirect(url_for('load_ec2.loadec2',rowinfo=str(rowid)+":"+form.awsregion.data))
    return render_template('load_ec2/ec2.html',title="EC2",form=form,row=rowid)

#Start ec2 instance
@blue.route('/startec2/<string:idinstance>',methods=['GET','POST'])
def startec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    status = ['running','pending','terminated']

    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_start_response = client.start_instances(InstanceIds=[instance_id])
        wait_loop = 40
        status_check = 'running'
        while wait_loop > 0:
            response = client.describe_instances(InstanceIds=[instance_id])
            if response['Reservations'][0]['Instances'][0]['State']['Name'] == status_check:
                break
            else:
                wait_loop = wait_loop - 1
            time.sleep(5)
        return jsonify({'result':'pass'})

#Stop ec2 instance
@blue.route('/stopec2/<string:idinstance>',methods=['GET','POST'])
def stopec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    ec2_client_resource = boto3.resource('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    status = ['pending','terminated','stopping','stopped','shutting-down']
   
    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_stop_response = client.stop_instances(InstanceIds=[instance_id])
        wait_loop = 40
        status_check = 'stopped'
        while wait_loop > 0:
            response = client.describe_instances(InstanceIds=[instance_id])
            if response['Reservations'][0]['Instances'][0]['State']['Name'] == status_check:
                break
            else:
                wait_loop = wait_loop - 1
            time.sleep(5)
        return jsonify({'result':'pass'})

#Terminate ec2 instance
@blue.route('/terminatec2/<string:idinstance>',methods=['GET','POST'])
def terminatec2(idinstance):
    # Get instance info
    instance_id = idinstance.split('_')[0]
    row_id = idinstance.split('_')[1].split(':')[0]
    region = idinstance.split('_')[1].split(':')[1]

    #get access info
    get_access_info = AccessKey.query.get(row_id)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    # check the status of instance
    client = boto3.client('ec2',region_name=region,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    #terminate status
    status = ['terminated','pending']

    if response['Reservations'][0]['Instances'][0]['State']['Name'] in status:
        return jsonify({'result':'fail'})
    else:
        ec2_terminate_response = client.terminate_instances(InstanceIds=[instance_id])
        wait_loop = 40
        status_check = 'terminated'
        while wait_loop > 0:
            response = client.describe_instances(InstanceIds=[instance_id])
            if response['Reservations'][0]['Instances'][0]['State']['Name'] == status_check:
                break
            else:
                wait_loop = wait_loop - 1
            time.sleep(5)
        return jsonify({'result':'pass'})

# View EC2 info
@blue.route('/viewinfo/<string:idinstance>',methods=['GET','POST'])
def viewinfo(idinstance):
    awsregion = idinstance.split(":")[1]
    row = idinstance.split(":")[2]
    instance_id = idinstance.split(":")[0]

    #get access info
    get_access_info = AccessKey.query.get(row)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    client = boto3.client('ec2',region_name=awsregion,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    instance_data = response['Reservations']
    
    #ami
    ami_info = client.describe_images(Filters=[{'Name':'image-id','Values':[instance_data[0]['Instances'][0]['ImageId']]}])

    #security groups
    sg_id = instance_data[0]['Instances'][0]['SecurityGroups'][0]['GroupId']
 
    sg = client.describe_security_groups(Filters=[{'Name':'group-id','Values':[sg_id]}])
    sg_data = sg['SecurityGroups'][0]
    
    #volume
    volume = client.describe_volumes(Filters=[{'Name':'attachment.instance-id','Values':[instance_id]}])
    volume_data = volume['Volumes']
        
    return render_template('load_ec2/viewinfo.html',title="EC2 View Info",awsregion=awsregion,row=row,instance_id=instance_id,instance_data=instance_data,ami_info=ami_info,
    sg_data=sg_data,volume_data=volume_data)

#SSH EC2 instance
@blue.route('/sshec2/<string:idinstance>',methods=['GET','POST'])
def sshec2(idinstance):
    form = Ec2SshForm()
    awsregion = idinstance.split(":")[1]
    row = idinstance.split(":")[2]
    instance_id = idinstance.split(":")[0]

    #get access info
    get_access_info = AccessKey.query.get(row)

    #get accesskey and secretkey
    accesskey = get_access_info.accesskeyid
    secretkey = get_access_info.secretkeyid

    client = boto3.client('ec2',region_name=awsregion,aws_access_key_id=accesskey,aws_secret_access_key=secretkey)
    response = client.describe_instances(InstanceIds=[instance_id])
    instance_data = response['Reservations']
    publicip = instance_data[0]['Instances'][0]['PublicIpAddress']

    if form.validate_on_submit():
        password_bytes = form.password.data.encode("ascii")
        base64_bytes = base64.b64encode(password_bytes)
        base64_password = base64_bytes.decode("ascii")
        #web ssh
        ssh_url = "http://localhost:8889/?hostname="+form.hostname.data+"&username="+form.username.data+"&password="+base64_password+"&title="+form.title.data
        webbrowser.open_new_tab(ssh_url)
        
    return render_template('load_ec2/sshec2.html',title='SSH EC2',awsregion=awsregion,row=row,instance_id=instance_id,form=form,publicip=publicip)
