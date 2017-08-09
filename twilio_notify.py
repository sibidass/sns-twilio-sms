import json
import logging

import boto3

import twilio_api

logger=logging.getLogger()
logger.setLevel(logging.INFO)

ec2 = boto3.client('ec2',region_name='ap-south-1')
def lambda_handler(event, context):
    event_dict = dict(event)
    logger.info(event_dict)
    msg_segment = ' '.join(event_dict['Records'][0]['Sns']['TopicArn'].split('_')[1:])
    null = 'Null'
    msg_dict = dict(json.loads(x['Records'][0]['Sns']['Message']))
    alarm_state = msg_dict['NewStateValue']
    if alarm_state == 'ALARM':
        state = 'CRITICAL'
    else:
        state = 'OK'
    metric_name = msg_dict['Trigger']['MetricName']
    instance_id = get_instance_id(msg_dict['Trigger']['Dimensions'])
    instance_name = get_instance_name(instance_id)
    msg_statement = msg_dict['NewStateReason']
    msg_body = state+':'+metric_name+' on '+instance_name+':'+msg_statement
    logger.info("Will send the following message:")
    logger.info("message body: "+msg_body)
    logger.info("segment: "+msg_segment)
    #twilio_api.send_sms(msg_segment,msg_body)


def get_instance_id(dimension_list):
    for dimension in dimension_list:
        if dimension['name'] == 'InstanceId':
            instance_id = dimension['value']
    return instance_id

def get_instance_name(instance_id):
    response = ec2.describe_instances(InstanceIds=[instance_id])
    response_tags = response['Reservations'][0]['Instances'][0]['Tags']
    for tag in response_tags:
        if tag['Key'] == 'Name':
            instance_name = tag['Value']
    return instance_name