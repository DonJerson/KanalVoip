import React, { Component } from 'react';
import Calendar from './Calendar';

const getUrl = window.location;
let host
if(getUrl.host.includes(":")){
  host = getUrl.host.substring(0, getUrl.host.length - 5);
}else{host = getUrl.host;}

let baseUrl
baseUrl = getUrl.protocol+ "//" + host +":9091/";

// if(window.location.includes("dialpro.net") ||  getUrl.protocol==="https:"){
//   baseUrl = getUrl.protocol+ "//" + host +":9091/";
//   console.log("dialpro.net")
// }else{
//   console.log("bobo.net",window.location)
//   baseUrl = getUrl.protocol+ "//" + host +":9091/";
// }

const axios = require('axios');
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.withCredentials = false;

var dateFormat = require('dateformat');
function formatNumber(num) {
  return num.toString().replace(/(\d)(?=(\d{3})+(?!\d))/g, '$1,')
}

const TableLineUser=(props)=>{
    const deleteUser=(e)=>{
      e.preventDefault()
      props.deleteUser(props.username)
    }
    return(
      <>
      <tr>           
        <td>{props.username}</td>
        <td>{props.password}</td>
        <td><a onClick={props.userPack.methods.deleteUser} href="/" style={{position:"relative",bottom:"28px"}}><img style={{width:"30px",height:"30px"}}src="svg/delete.svg" alt="Kiwi standing on oval" className="deleteIcon"/></a>-</td>
        </tr>
      </>
    )
  }
  const UserLine=(props)=>{
    const handleSelect=(e)=>{
      e.preventDefault()
      props.handleSelect(props.username)
    }
    let isSelected =false
    props.selectedUsers.forEach(user => {
      if(user===props.username){
        isSelected=true
      }
    });
    return(
      <>
      <a href="#" style={{backgroundColor:isSelected?"rgb(0, 112, 186)":"",color:isSelected?"white":""}}onClick={handleSelect}>{props.username}</a>
      <hr className="solid"></hr>
      </>
    )
  }
  const TableLineRecarga=(props)=>{
    const fecha = dateFormat(new Date(props.line.date), "dd/mm/yy @ HH:MM")
    //console.log(props.line,"line")
    return(
      <>
      <tr> 
        <td>{fecha}</td>
        <td>{parseFloat(props.line.amount).toFixed(2)}</td>
        </tr>
      </>
    )
  }

  const TableLineUsage=(props)=>{
    console.log(new Date(props.line.startTime))
    const fecha = dateFormat(new Date(props.line.startTime), "dd/mm/yy @ HH:MM:ss - ")+dateFormat(new Date(props.line.endTime), "HH:MM:ss")
    //console.log(props.line,"line")
    return(
      <>
      <tr> 
        <td>{props.line.src_user}</td>
        <td>{props.line.dst_user}</td>
        <td>{fecha}</td>
        <td>{props.line.duration}</td>
        <td>{parseFloat(props.line.duration*0.0144/60).toFixed(7)}</td>
        </tr>
      </>
    )
  }

let myUserId
class DashBoard extends Component {
    state={customer:false}
    
    constructor(props){
      super(props)
      myUserId=props.userId

    }
    componentWillMount(props){
      console.log(props)
      if(myUserId){
        axios.post(baseUrl + `getSubscriberAdmin/`,{userId:myUserId}).then(res=>{
          if(res.data.id){
            console.log("success set",res.data.id)
            this.props.userPack.virtualUpdate(res.data)
          }
        }).catch(err=>{
          console.log("error nuevo",err)
        })
      }
    }
    render() { 
     
        let showing
        const isMobile=this.props.userPack.dimensions.width<768
        let marginBody = this.props.userPack.dimensions.isMobile?"15px":"50px"
        let display
        let recargasHistory=this.props.userPack.recargasHistory
        console.log(recargasHistory, "recargasHistory")
        //console.log(this.props.usethis.rPack.userPack.selectedUsers.length, "length")
        if((this.props.userPack.filteredResults)&&(this.props.userPack.filteredResults.length>0  ||this.props.userPack.selectedUsers.length>0)){
          display=this.props.userPack.filteredResults
          showing = this.props.userPack.filteredResults.length
        }else{
          display=this.props.userPack.history
          showing = this.props.userPack.amountCalls
        }
        let customer
        if(this.state&& this.state.customer){
          customer = this.state.customer
        }else{
          customer=this.props.userPack.customer
        }
        console.log("hishis",this.props.userPack.history)
        return ( <>
        <div id="mainBody" style={{marginLeft:marginBody,marginRight:marginBody,marginTop:"18px",marginBottom:"200px"}}>
        <div className="row">
              <h1 className="mainTitle" style={{marginLeft:"10px",fontSize:isMobile?"40px":"40px"}}>Welcome {customer.name}</h1>
            </div> 

            <div className="row" style={{paddingTop:"10px",marginLeft:isMobile?"0.3rem":"0px",marginRight:isMobile?"0.3rem":"0px"}}>

              <div className="col-xs-12 col-sm-4 caja" style={{maxHeight:"140px",paddingTop:"10px"}}>
                
                <div className="row center">
                <h1 className="balance">US${parseFloat(customer.balance).toFixed(2)}</h1>
                </div>
                <div className="row center" style={{marginTop:"5px"}}>
                  <div className="col-xs-auto">
                <button onClick={this.props.userPack.methods.recargar} style={{marginTop:"8px",width:"150px",position:"relative",bottom:"6px"}}className="pure-material-button-contained green">Recargar</button>
                </div>
                  </div>
                  <div className="row center" style={{marginTop:"5px"}}>
                  <a href="wa.link/cfydhk"><p> Whatsapp Support: (561) 872-8037</p></a>
                </div>
              </div>
              <div className="col-xs-12 col-sm-7 caja" style={{marginRight:"0px",marginLeft:isMobile?"0.0px":this.props.userPack.dimensions.width*0.065+"px",marginTop:!isMobile?"0px":"25px",paddingTop:"10px",paddingBottom:"10px"}}>
              <div className="row center">
                <div className="col-xs-auto">
                <h1 className="secondTitle" style={{marginBottom:"5px",fontSize:isMobile?"28px":"30px"}}>Mis dispositivos</h1><button onClick={this.props.userPack.methods.addDevice} style={{marginLeft:"35px",width:"100px",position:"relative",bottom:"6px"}}className="pure-material-button-contained">Agregar</button>
                </div>
                </div>
                <div className="row center">
                {/* <p className="infoText">Saldo Actual</p> */}
                <table id="customers">
                <thead>
                <tr>
                <th>USUARIO</th>
                <th>CONTRASEÑA</th>
                <th>IP</th>
              </tr>
              </thead>

              <tbody>

              {this.props.userPack.loadingComponent?
                       null
                :
                <>
                {customer.subscribers.map((subscriber,index)=>(
                  <TableLineUser userPack={this.props.userPack} deleteUser={this.deleteUser} key={subscriber.id} username={subscriber.username} password={subscriber.password}/>
            ))} 
            </>
                }


              </tbody>

            </table>
            {this.props.userPack.loadingComponent?
                        <div className="row center">
                          <div className="col-xs-auto">
                            <div className="lds-hourglass" ></div>
                          </div>
                        
                         
                       </div>
                :
                null} 
                </div>
                </div>
              
            </div>
            <div className="row" style={{marginTop:"30px"}}>
            <div className="col-xs-auto" style={{marginLeft:"10px"}}>
            <div className="dropdown">
              <button className="dropbtn">Usuarios</button>
              <div className="dropdown-content" >
              {customer.subscribers.map((subscriber,index)=>(
                  <UserLine userPack={this.props.userPack} selectedUsers={this.props.userPack.selectedUsers} handleSelect={this.props.userPack.methods.handleSelect} key={subscriber.id} username={subscriber.username} password={subscriber.password}/>
            ))} 
              </div>
              </div>
            </div>
            <div className="col-xs-auto">
            <div className="dropdown" style={{marginLeft:"15px"}}>
              <button className="dropbtn">Inicio</button>
              <div className={"dropdown-content left"} >
                <Calendar/>
              </div>
              </div>
            </div>
            <div className="col-xs-auto">
            <div className="dropdown" style={{marginLeft:"15px"}}>
              <button className="dropbtn">Final</button>
              <div className="dropdown-content right" >
              <Calendar/>
              </div>
              </div>
            </div>

            </div>
            
                        <div className="row" style={{marginLeft:"8px",marginTop:"16px"}}>
                        <input type="search" value={this.props.userPack.filterNumber} placeholder="Buscar por número" onChange={this.props.userPack.methods.filterNumber}/>


                        </div>
            
            
            <div className="col-xs-12 caja" style={{marginTop:"25px",marginBottom:"80px",overflowX:"visible"}}>
                
                <div className="row">
                <div className="col-xs-12 col-md-6" >
                <h1 className="secondTitle" style={{marginTop:"10px",padding:"8px",fontSize:isMobile?"24px":"34px"}}>Historial de llamadas               </h1>

                </div>
                <div className="col-xs-12 col-md-6">
                {this.props.userPack.dimensions.width<1024?
                        <div className="col-xs-auto">
                        {/* Total consumido: {this.totalConsumido} */}
                        
                        <p style={{paddingTop:"8px",paddingBottom:"8px"}}>Mostrando {formatNumber(showing)} de {formatNumber(this.props.userPack.totalCalls)} llamadas <a href="#" onClick={this.props.userPack.methods.fetchMore}>ver más </a></p>
                        </div>
            :                        <div className="col-xs-auto" style={{position:"absolute",right:"70px"}}>
            {/* Total consumido: {this.totalConsumido} */}
            
            <p style={{paddingTop:"5px"}}>Mostrando {formatNumber(showing)} de {formatNumber(this.props.userPack.totalCalls)} llamadas <a href="#" onClick={this.props.userPack.methods.fetchMore}>ver más </a></p>
            </div>
            }
</div>
                </div>
                <div className="row center">
                {/* <p className="infoText">Saldo Actual</p> */}
                <table id="customers" style={{overflowX:"scroll !important"}}>
                <thead>
                <tr>
                <th>Desde</th>
                <th>Hacia</th>
                <th>Fecha</th>
                <th>Duración (segundos)</th>
                <th>Costo (US$)</th>
                
              </tr>
              </thead>
              <tbody>
                {this.props.userPack.loadingHistorial?
                  null
                :
                
                display.map((log,index)=>(
                  <TableLineUsage line={log} key={index}/>
            ))
                } 


              </tbody>
              
            </table>
              {this.props.userPack.loadingHistorial?
                        <div className="row center">
                          <div className="col-xs-auto">
                            <div className="lds-hourglass" ></div>
                          </div>
                        
                         
                       </div>
                :
                null} 
                </div>
              </div>



              <div className="col-xs-12 caja" style={{marginTop:"25px",marginBottom:"80px",overflowX:"visible"}}>
                
                <div className="row">
                <div className="col-xs-12 col-md-6" >
                <h1 className="secondTitle" style={{marginTop:"10px",padding:"8px",fontSize:isMobile?"24px":"34px"}}>Historial de recargas               </h1>

                </div>
                <div className="col-xs-12 col-md-6">
                {this.props.userPack.dimensions.width<1024?
                        <div className="col-xs-auto">
                        {/* Total consumido: {this.totalConsumido} */}
                        
                        <p style={{paddingTop:"8px",paddingBottom:"8px"}}>Mostrando {formatNumber(recargasHistory.length)} de {formatNumber(recargasHistory.length)} recargas</p>
                        </div>
            :                        <div className="col-xs-auto" style={{position:"absolute",right:"70px"}}>
            {/* Total consumido: {this.totalConsumido} */}
            
            <p style={{paddingTop:"5px"}}>Mostrando {formatNumber(recargasHistory.length)} de {formatNumber(recargasHistory.length)} recargas</p>
            </div>
            }
</div>
                </div>
                <div className="row center">
                {/* <p className="infoText">Saldo Actual</p> */}
                <table id="customers" style={{overflowX:"scroll !important"}}>
                <thead>
                <tr>
                <th>Fecha</th>
                <th>Monto (US$)</th>
                
              </tr>
              </thead>
              <tbody>
                {this.props.userPack.loadingHistorial?
                  null
                :
                
                recargasHistory.reverse().map((log,index)=>(
                  <TableLineRecarga line={log} key={index}/>
            ))
                } 


              </tbody>
              
            </table>
              {this.props.userPack.loadingHistorial?
                        <div className="row center">
                          <div className="col-xs-auto">
                            <div className="lds-hourglass" ></div>
                          </div>
                        
                         
                       </div>
                :
                null} 
                </div>
              </div>


            {/* <div classname="row">
              <h1 className="mainGrayTitle">Mis dispositivos</h1>
            </div>
            {customer.subscribers.map((subscriber,index)=>(
                          <div classname="row" style={{backgroundColor:"#5e5c5b"}}>
                          <p style={{color:"white"}}>Username: {subscriber.username} Password: {subscriber.password} </p>
                        </div>
            ))} */}

        </div>


        
        </> );
    }
}
 
export default DashBoard;

