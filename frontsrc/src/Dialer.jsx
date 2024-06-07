import React, { Component } from 'react';

const SIP = require("sip.js");

const config = {
    // Replace this IP address with your Asterisk IP address
    uri: '1060@dialerprieto.xyz',
  
    // Replace this IP address with your Asterisk IP address,
    // and replace the port with your Asterisk port from the http.conf file
    ws_servers: 'wss://dialerprieto.xyz:8089/ws',
  
    // Replace this with the username from your sip.conf file
    authorizationUser: '1060',
  
    // Replace this with the password from your sip.conf file
    password: 'W3lcome77@@',
  };
  



class Dialer extends Component {
    state = {  }
    constructor(props){
        super(props)
        let calls = []
        this.state={calls}
    }
    componentDidMount(){
        let calls = []
        // let userAgent = new UA({
        //     uri: '1060@172.81.181.5',
        //     authorizationUser: '1060',
        //     password: 'W3lcome77@@'
        //   });
        //   userAgent.subscribe('1060@172.81.181.5', 'presence')
        //   userAgent.on('invite', (session) => {
        //         calls.push(session)
        //         console.log(session)
        //         //session.accept()
        //     });
        // console.log(userAgent)
        let userAgent = new SIP.UA(config);
  
        // Invite with audio only
        userAgent.invite('1061',{
          sessionDescriptionHandlerOptions: {
            constraints: {
              audio: true,
              video: false
            }
          }
        });
        this.setState({userAgent})
    }
    render() { 
        return ( <>
        
        <h1>Qloq</h1>
        {this.state.calls.map(call=>(
            <p>{call}</p>
        ))}
        
        </> );
    }
}
 
export default Dialer;