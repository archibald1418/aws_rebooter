import { LightsailClient, RebootInstanceCommand } from "@aws-sdk/client-lightsail";

const lightsail = new LightsailClient({region: 'us-east-1'});
var input = {
    instanceName: process.env.INSTANCE_NAME
}

const cmd = new RebootInstanceCommand(input);
export const handler = async(event) => {
    try {
        const operations = await lightsail.send(cmd);
        console.info(operations);
        return {
            statusCode: 200,
            body: JSON.stringify('Your instance was rebooted successfully')
        };
    } catch (e) {
        // console.error(e);
        // throw e;
        return {
            statusCode: 500,
            body: JSON.stringify("Something bad happened with your lambda... see logs")
        };
    }
};
