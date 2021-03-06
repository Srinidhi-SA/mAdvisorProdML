import React from "react";
import {MainHeader} from "../common/MainHeader";
import {connect} from "react-redux";
import {Link, Redirect} from "react-router-dom";
import store from "../../store";
import {Modal,Button,Tabs,Tab,Row,Col,Nav,NavItem,Form,FormGroup,FormControl} from "react-bootstrap";
import {createModel,getRegressionAppAlgorithmData,setDefaultAutomatic,updateAlgorithmData,checkAtleastOneSelected,saveParameterTuning,changeHyperParameterType, pytorchValidateFlag, setPyTorchSubParams,updateTensorFlowArray} from "../../actions/appActions";
import {AppsLoader} from "../common/AppsLoader";
import {getDataSetPreview} from "../../actions/dataActions";
import {RegressionParameter} from "./RegressionParameter";
import {STATIC_URL} from "../../helpers/env.js";
import {statusMessages} from "../../helpers/helper";
import { TensorFlow } from "./TensorFlow";
import { PyTorch } from "./PyTorch";

@connect((store) => {
    return {login_response: store.login.login_response,
        dataPreview: store.datasets.dataPreview,
        modelTargetVariable:store.apps.modelTargetVariable,
        selectedAlg:store.apps.selectedAlg,
        scoreSummaryFlag:store.apps.scoreSummaryFlag,
        currentAppId:store.apps.currentAppId,
        automaticAlgorithmData:store.apps.regression_algorithm_data,
        manualAlgorithmData:store.apps.regression_algorithm_data_manual,
        isAutomatic:store.apps.regression_isAutomatic,
        apps_regression_modelName:store.apps.apps_regression_modelName,
        currentAppDetails:store.apps.currentAppDetails,
        modelSummaryFlag:store.apps.modelSummaryFlag,
        pytorchValidateFlag: store.datasets.pytorchValidateFlag,
        pyTorchLayer:store.apps.pyTorchLayer,
        pyTorchSubParams:store.apps.pyTorchSubParams,
        idLayer:store.apps.idLayer,
    };
})

export class ModelAlgorithmSelection extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            showParameterTuning:false
        };
    }
    componentWillMount() {
        if(this.props.apps_regression_modelName == "" || this.props.currentAppDetails == null){
            window.history.go(-1);
        }
    }
    componentDidMount() {
        $("#manualBlock_111").addClass("dispnone");
        $("#automaticBlock_111").removeClass("dispnone");

    }

    createModel(event){
        Notification.requestPermission();
            var isContinueRange = this.checkRangeValidation();
            var isContinueMulticheck = this.checkMultiSelectValidation();
            
            var tfFlag=this.props.manualAlgorithmData.filter(i=>i.algorithmName=="Neural Network (TensorFlow)")[0].selected
            
        if(!isContinueRange || !isContinueMulticheck){
             if(document.getElementsByClassName("InterceptGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Fit Intercept...","small_mascot");
                    bootbox.alert(msg);
                    $(".InterceptGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                }else if(document.getElementsByClassName("solverGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Solver Used...","small_mascot");
                    bootbox.alert(msg);
                    $(".solverGrid .multiselect").addClass("regParamFocus");

                    return false;   
                }else if(document.getElementsByClassName("criterionGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Criterion...","small_mascot");
                    bootbox.alert(msg);
                    $(".criterionGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                }else if(document.getElementsByClassName("bootstrapGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Bootstrap Sampling...","small_mascot");
                    bootbox.alert(msg);
                    $(".bootstrapGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                }else if(document.getElementsByClassName("boosterGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Booster Function...","small_mascot");
                    bootbox.alert(msg);
                    $(".boosterGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                }else if(document.getElementsByClassName("treeGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Tree Construction Algorithm...","small_mascot");
                    bootbox.alert(msg);
                    $(".treeGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                } else if(document.getElementsByClassName("activation")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Activation...","small_mascot");
                    bootbox.alert(msg);
                    $(".activation .multiselect").addClass("regParamFocus");
                    return false;
                }else if(document.getElementsByClassName("shuffleGrid")[0].innerHTML.includes("None selected") && (document.getElementsByClassName("solverGrid")[0].innerText.includes("adam") || document.getElementsByClassName("solverGrid")[0].innerText.includes("sgd") ) ){
                    let msg= statusMessages("warning","Please select Shuffle...","small_mascot");
                    bootbox.alert(msg);
                    $(".shuffleGrid .multiselect").addClass("regParamFocus");

                    return false;
                }else if((document.getElementsByClassName("learningGrid")[0].innerHTML.includes("None selected")) && (document.getElementsByClassName("solverGrid")[0].innerText.includes("sgd"))){
                    let msg= statusMessages("warning","Please select Learning Rate...","small_mascot");
                    bootbox.alert(msg);
                    $(".learningGrid .multiselect").addClass("regParamFocus");

                    return false;
                }else if(document.getElementsByClassName("batchGrid")[0].innerHTML.includes("None selected")){
                    let msg= statusMessages("warning","Please select Batch Size...","small_mascot");
                    bootbox.alert(msg);
                    $(".batchGrid .multiselect").addClass("regParamFocus");
                    
                    return false;
                }               
                let msg= statusMessages("warning","Please resolve errors...","small_mascot");
                bootbox.alert(msg);
                return false;
        }
        if(tfFlag){
       var tfInputs=store.getState().apps.tensorFlowInputs;
       let units= document.getElementsByClassName("units_tf")
       let rates= document.getElementsByClassName("rate_tf")
       var errMsgs=document.getElementsByClassName("error")
       var finalActivation = ["sigmoid","softmax"]
        for(let i=0; i<units.length; i++){
            var unitFlag;
            if(units[i].value==="")
            unitFlag = true;
           }
        
        for(let i=0; i<rates.length; i++){
            var rateFlag;
            if(rates[i].value==="")
            rateFlag = true;
           }
           
        for(let i=0; i<errMsgs.length; i++){
            var errMsgFlag;
            if(errMsgs[i].innerText!="")
            errMsgFlag = true;
            }

        if(tfInputs.length>1 && tfInputs[tfInputs.length-1].layer=="Dropout"){
        bootbox.alert(statusMessages("warning", "Final layer should be 'Dense' for TensorFlow.", "small_mascot"));
        return false
        }else if ($(".activation_tf option:selected").text().includes("--Select--")){
            bootbox.alert(statusMessages("warning", "Please select 'Activation' for dense layer in TensorFlow.", "small_mascot"));
            return false
        }else if(tfInputs.length>=1 && !finalActivation.includes(tfInputs[tfInputs.length-1].activation)){
            bootbox.alert(statusMessages("warning", "TensorFlow final Dense layer should have 'Softmax' or 'Sigmoid' for activation.", "small_mascot"));
            return false;
        }else if(unitFlag){
            bootbox.alert(statusMessages("warning", "Please enter 'Units' for dense layer in TensorFlow.", "small_mascot"));
            return false;
        }else if($(".batch_normalization_tf option:selected").text().includes("--Select--")){
            bootbox.alert(statusMessages("warning", "Please select 'Batch Normalisation' for dense layer  in TensorFlow.", "small_mascot"));
            return false;            
        }else if(rateFlag){
            bootbox.alert(statusMessages("warning", "Please enter 'Rate' for dropout layer in TensorFlow.", "small_mascot"));
            return false;
        }else if(errMsgFlag){
            bootbox.alert(statusMessages("warning", "Please resolve errors for TensorFlow.", "small_mascot"));
            return false;
        }
       
        if(this.props.currentAppId === 2 && tfInputs.length>=1 && tfInputs[tfInputs.length-1].layer=="Dense"){
            this.props.dispatch(updateTensorFlowArray(tfInputs.length,"units",store.getState().apps.targetLevelCounts.length.toString()))
        }else if(this.props.currentAppId === 13 && tfInputs.length>=1 && tfInputs[tfInputs.length-1].layer=="Dense"){
            this.props.dispatch(updateTensorFlowArray(tfInputs.length,"units",1))
        }
        
    }
        var pyTorchClassFlag = false;
        var targetCount;
        var pyTorchLayerCount;
        if(this.props.currentAppId === 2 && this.props.automaticAlgorithmData.filter(i=>i.algorithmName==="Neural Network (PyTorch)")[0].selected){
            pyTorchClassFlag = true;
            targetCount = store.getState().apps.targetLevelCounts;
            pyTorchLayerCount = Object.keys(this.props.pyTorchLayer).length;
        }
        let errormsg = statusMessages("warning","Please Enter Mandatory Fields of PyTorch Algorithm...","small_mascot");
        if(pyTorchClassFlag){
            if(!this.props.pytorchValidateFlag){
                bootbox.alert(errormsg);
                return false;
            }
            else if( ($(".loss_pt")[0].value === "None") || ($(".optimizer_pt")[0].value === "None") || ($(".regularizer_pt")[0].value === "None") ){
                bootbox.alert(errormsg);
                return false;
            }
            else if(pyTorchLayerCount === 0){
                bootbox.alert(statusMessages("warning", "Please Add Layers for PyTorch", "small_mascot"));
                return false;
            }
            else if((pyTorchLayerCount != 0) && ( (this.props.pyTorchLayer[pyTorchLayerCount].units_op < targetCount.length) || (this.props.pyTorchLayer[pyTorchLayerCount].units_op > targetCount.length) )){
                bootbox.alert(statusMessages("warning", "No. of output units in Pytorch final layer should be equal to the no. of levels in the target column(which is "+targetCount.length+").", "small_mascot"));
                return false;
            }
            else if( (pyTorchLayerCount != 0) && $(".activation_pt")[pyTorchLayerCount-1].value != "Sigmoid" && ( $(".loss_pt")[0].value === "NLLLoss" || $(".loss_pt")[0].value === "BCELoss") ){
                this.props.dispatch(pytorchValidateFlag(false));
                bootbox.alert(statusMessages("warning", "Activation should be Sigmoid as Loss selected is"+$(".loss_pt")[0].value+"", "small_mascot"));
                return false;
            }
            for(let i=0;i<pyTorchLayerCount;i++){
                if(document.getElementsByClassName("input_unit_pt")[i].value === ""){
                    bootbox.alert(errormsg);
                    return false;
                }
                else if(document.getElementsByClassName("output_unit_pt")[i].value === ""){
                    bootbox.alert(errormsg);
                    return false;
                }
                else if($(".bias_init_pt option:selected")[i].value === "None"){
                    bootbox.alert(errormsg);
                    return false;
                }
                else if($(".weight_init_pt option:selected")[i].value === "None"){
                    bootbox.alert(errormsg);
                    return false;
                }
            }
            if(this.props.pytorchValidateFlag && ( $(".optimizer_pt option:selected").text().includes("Adam") || $(".optimizer_pt option:selected").text().includes("AdamW") || $(".optimizer_pt option:selected").text().includes("SparseAdam") || $(".optimizer_pt option:selected").text().includes("AdamW") || $(".optimizer_pt option:selected").text().includes("Adamax") ) ){
                let beta = this.props.pyTorchSubParams;
                let tupVal = beta["optimizer"]["betas"].toString();
                beta["optimizer"]["betas"] = "("+ tupVal + ")";
                this.props.dispatch(setPyTorchSubParams(beta));
            }
            else if(this.props.pytorchValidateFlag && $(".optimizer_pt option:selected").text().includes("Rprop")){
                let eta = this.props.pyTorchSubParams;
                let tupVal1 = eta["optimizer"]["eta"].toString();
                eta["optimizer"]["eta"] = "("+ tupVal1 + ")";
                this.props.dispatch(setPyTorchSubParams(eta));
    
                let tupVal2 = eta["optimizer"]["step_sizes"].toString();
                eta["optimizer"]["step_sizes"] = "("+ tupVal2 + ")";
                this.props.dispatch(setPyTorchSubParams(eta));
            }
        }
        this.props.dispatch(createModel(store.getState().apps.apps_regression_modelName,store.getState().apps.apps_regression_targetType,store.getState().apps.apps_regression_levelCount,store.getState().datasets.dataPreview.slug,"analyst"));
    }
    handleOptionChange(e){
        if(e.target.value == 1){
         $("#automaticBlock_111").removeClass("dispnone");
          $("#manualBlock_111").addClass("dispnone");
        }
        else
        {
            $("#automaticBlock_111").addClass("dispnone");
          $("#manualBlock_111").removeClass("dispnone");
        }
        this.props.dispatch(setDefaultAutomatic(e.target.value));
    }
    changeAlgorithmSelection(data){
        this.props.dispatch(updateAlgorithmData(data.algorithmSlug));
    }
    changeParameter(){
        this.props.dispatch(saveParameterTuning());
    }
    changeHyperParameterType(slug,e){
        this.props.dispatch(changeHyperParameterType(slug,e.target.value));
        if(e.target.value="none"){
            $(".learningGrid .for_multiselect").removeClass("disableGrid");
        }
    }

    handleBack=()=>{
        const appId = this.props.match.params.AppId;
        const slug = this.props.match.params.slug;
        this.props.history.replace(`/apps/${appId}/analyst/models/data/${slug}/createModel/algorithmSelection`);

      }

    render() {
        if(store.getState().apps.modelSummaryFlag){ 
            var modeSelected= store.getState().apps.analystModeSelectedFlag?'/analyst' :'/autoML'
            let _link = "/apps/"+store.getState().apps.currentAppDetails.slug+modeSelected+'/models/'+store.getState().apps.modelSlug;
            return(<Redirect to={_link}/>);
        }
        var algorithmData = this.props.manualAlgorithmData;
        var algoClass = (this.props.currentAppId == 13) ? "col-md-3" : "col-md-algo";
        if (!$.isEmptyObject(algorithmData)){
            var pageData = "";
                var buttonName = "Create Model";
                var pageTitle = "Parameter Tuning";
                var label= document.getElementsByClassName("active")[1];
                var minmaxLabel= (label=== undefined) ? "linear" : label.innerText 
               
                var pageData = algorithmData.map((data,Index) =>{
                    var hyperParameterTypes = [];
                    var selectedValue = "";
                    var hyperparameterOptionsData = "";
                    var algorithmPath = "algorithmData["+Index+"]";
                    var options = data.hyperParameterSetting;
                        for (var prop in options) {
                            if(options[prop].selected){
                                selectedValue = options[prop].name;
                                if(options[prop].params != null && options[prop].params.length >0){
                                    var hyperparameterOptions = options[prop].params;
                                    hyperparameterOptionsData = hyperparameterOptions.map((param,index) =>{
                                        if(param.display){
                                            return(

                                                    <div class="form-group">
                                                        <label class="col-md-3 control-label read">{param.displayName}</label>
                                                        <RegressionParameter parameterData={param} tuneName={selectedValue} algorithmSlug={data.algorithmSlug} type="TuningOption"/>
                                                    <div class="clearfix"></div>
                                                    </div>

                                            );
                                        }
                                    });
                                }
                            }
                            hyperParameterTypes.push(<option key={prop} className={prop} value={options[prop].name}>{options[prop].displayName}</option>);
                        }
                    var algorithmParameters = data.parameters;
                    if(selectedValue != "none"){
                        var parametersData = algorithmParameters.map((params,Index) =>{
                            if(params.hyperpatameterTuningCandidate && params.display){
                                return(

                                        <div class="form-group">
                                            <label class="col-md-2 control-label read">{params.displayName}</label>
                                            <label class="col-md-4 control-label read">{params.description}</label>
                                            <RegressionParameter parameterData={params} tuneName={selectedValue} algorithmSlug={data.algorithmSlug} isTuning={true} type="TuningParameter"/>
                                        <div class="clearfix"></div>
                                        </div>

                                );
                            }
                        });
                    }
                    else
                    {
                        var parametersData = algorithmParameters.map((params,Index) =>{
                            if(params.display){
                                return(

                                    <div class="form-group">
                                        <label class="col-md-2 control-label read">{params.displayName}</label>
                                        <label class="col-md-4 control-label read">{params.description}</label>
                                        <RegressionParameter parameterData={params} tuneName={selectedValue} algorithmSlug={data.algorithmSlug} type="NonTuningParameter"/>
                                    <div class="clearfix"></div>
                                    </div>

                                );
                            }
                        });
                    }
                    if(data.selected == true)
                    {
                        return(
                            <Tab eventKey={data.algorithmSlug} title={data.algorithmName}>
                                <FormGroup role="form">
                                {data.algorithmName === "Neural Network (TensorFlow)"?
                                <TensorFlow data/>
                                :data.algorithmName === "Neural Network (PyTorch)"?
                                <PyTorch parameterData={data} type="NonTuningParameter"/>:
                                (
								 <div className="xs-mt-20">
                                    <div className="form-group">
                                    <label class="col-md-3 control-label">Hyperparameter Tuning :</label>
                                    <div className="col-md-3">
                                        <select  class="form-control hyperTune" onChange={this.changeHyperParameterType.bind(this,data.algorithmSlug)} value={selectedValue}>
                                        {hyperParameterTypes}
                                        </select>
                                    </div>
                                    <div class="clearfix"></div>
                                    </div>
                                 </div>)}
                                 {(data.algorithmName === "Neural Network (TensorFlow)") || (data.algorithmName === "Neural Network (PyTorch)")?"":
                                 (<span>
                                <div>{hyperparameterOptionsData}</div>
                                <div>
                                    <div className="col-md-12">
                                    {selectedValue != "none"?
                                    <h5 className="text-info xs-mb-20">You can provide the intervals or options that we use for optimization using hyperparameter tuning.</h5>
                                    :<h5 className="text-info xs-mb-20">The parameter specifications below are recommended by mAdvisor.  You can still go ahead and tune any of them.</h5>}
                                    </div>
                                 </div>
                                 </span>)}
                                {selectedValue != "none" && (minmaxLabel != "LINEAR REGRESSION")?
                                <div className="maxminLabel">
                                     <label class="col-md-6 control-label read"></label>
                                     <label class="col-md-1 control-label read text-center">
                                            <b>Min</b>
                                    </label>
                                     <label class="col-md-1 control-label read text-center">
                                         <b>Max</b>
                                    </label>
                                     <label class="col-md-4 control-label read"><b><span>Enter values in one or multiple intervals</span></b></label>
                                </div>:""}
                                
                                <div>{(data.algorithmName === "Neural Network (TensorFlow)") || (data.algorithmName === "Neural Network (PyTorch)")?"":parametersData}</div>
								</FormGroup>
                            </Tab>
                        );
                    }

                });
            // }

        return(
                <div className="side-body">
                    <div className="page-head">

                                <h3 class="xs-mt-0 text-capitalize">{pageTitle}</h3>

                    </div>
                    <div className="main-content">
                          <div className="panel panel-mAd xs-p-20 box-shadow">
                                {/* {this.state.showParameterTuning == false ?
                                <div>
                                    <div className="panel-heading xs-ml-0 xs-mb-10">
                                        Please use the following learning algorithms for prediction
                                    </div>
                                    <div className="panel-body no-border">
									<div className="row algSelection xs-mb-20">
                                     {pageData}
									 </div>
                                     </div>
                                </div>:


                            } */}
                               <Tabs  id="algosel" onSelect={this.changeParameter.bind(this)} className="tab-container">
                                {pageData}
                                </Tabs>
							<div className="clearfix"></div>
                            <div>
                            <Button onClick={this.handleBack} bsStyle="primary"><i class="fa fa-angle-double-left"></i> Back</Button>
                            <Button id="parameterCreateModel" type="button" bsStyle="primary xs-pl-20 xs-pr-20" style={{float:'right'}} onClick={this.createModel.bind(this)}>{buttonName} <i class="fa fa-angle-double-right"></i></Button>
                            </div>
							<div className="clearfix"></div>
                         </div>
                    </div>
                    <AppsLoader match={this.props.match}/>
                </div>
        );
    }
    else{
        return (
                 <div className="side-body">
                    <div className="page-head">
                    </div>
                    <div className="main-content">
                      <img id="loading" src={ STATIC_URL + "assets/images/Preloader_2.gif" } />
                    </div>
                  </div>
                );
    }
    }
    checkRangeValidation(){
        var isGo = true;
        $('.range-validate').each(function(){
            if($(this)[0].innerHTML != "")
            isGo =false;
        });
        return isGo;
    }
    checkMultiSelectValidation(){
        var isGo = true;
        $('.check-multiselect').each(function(){
            if($(this)[0].innerHTML != "")
            isGo =false;
        });
        return isGo;
    }
}
