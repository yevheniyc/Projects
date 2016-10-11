function retrieveSymmetryData(pdbid,bioassembly){var bionumber=bioassembly2bionumber(bioassembly);var basePath="/pdb/json/symmetryOrientation";var url=basePath+"?pdbID="+pdbid+"&bioassembly="+bionumber;return xhrPromise(url,"json");}
function bionumber2bioassembly(bionumber){if(!bionumber||bionumber==="asym"){return"__AU";}else{return"BU"+bionumber;}}
function bioassembly2bionumber(bioassembly){if(!bioassembly||bioassembly==="__AU"){return"asym";}else{return bioassembly.substr(2);}}
var SymmetryBuffer=function(axes,params){var p=Object.assign({},params);var c=new NGL.Color(p.color||"lime");var radius=p.radius||0.5;var shape=new NGL.Shape("symmetry",{disableImpostor:true,openEnded:true});axes.forEach(function(ax){shape.addSphere(ax.start,c,radius);shape.addSphere(ax.end,c,radius);shape.addCylinder(ax.start,ax.end,c,radius);});this.attach=function(component){shapeRepr=component.addBufferRepresentation(shape.getBufferList());};this.dispose=function(){if(shapeRepr)shapeRepr.dispose();};};var NglController=function(id,params){var signals={taskCountChanged:new NGL.Signal(),fullscreenChanged:new NGL.Signal(),structureChanged:new NGL.Signal(),symmetryDataLoaded:new NGL.Signal(),colorSchemeChanged:new NGL.Signal(),modelChanged:new NGL.Signal(),hydrogenVisibilityChanged:new NGL.Signal(),ionVisibilityChanged:new NGL.Signal(),waterVisibilityChanged:new NGL.Signal(),qualityChanged:new NGL.Signal(),assemblyChanged:new NGL.Signal(),symmetryChanged:new NGL.Signal(),styleChanged:new NGL.Signal(),ligandStyleChanged:new NGL.Signal(),clicked:new NGL.Signal(),hovered:new NGL.Signal()};var pdbid;var structureComponent;var symmetryBuffer;var symmetryData={};var atomCount;var instanceCount;var axesRepr;var isBackboneOnly;var p=Object.assign({},params);var colorScheme=p.colorScheme||"chainname";var assembly=p.assembly||"BU1";var style=p.style||"cartoon";var ligandStyle=p.ligandStyle||"spacefill";var model=p.model||0;var symmetry=p.symmetry||0;var hydrogenVisibility=p.hydrogenVisibility===undefined?true:p.hydrogenVisibility;var ionVisibility=p.ionVisibility===undefined?false:p.ionVisibility;var waterVisibility=p.waterVisibility===undefined?false:p.waterVisibility;var quality=p.quality===undefined?"auto":p.quality;var spin=p.spin===undefined?false:p.spin;var stage=new NGL.Stage(id,{backgroundColor:"white",hoverTimeout:500});this.stage=stage;stage.signals.fullscreenChanged.add(function(fullscreen){signals.fullscreenChanged.dispatch(fullscreen);});stage.signals.clicked.add(function(pickingData){signals.clicked.dispatch(pickingData);});stage.signals.hovered.add(function(pickingData){signals.hovered.dispatch(pickingData);});window.addEventListener("resize",function(){stage.handleResize();},false);var tasks=new NGL.Counter();tasks.listen(stage.tasks);tasks.signals.countChanged.add(function(delta,count){signals.taskCountChanged.dispatch(delta,count);});setSpin(spin);var polymerReprDict={};var polymerReprDefs={"unitcell":{disableImpostor:true,radiusSegments:16},"cartoon":{colorScheme:function(){return colorScheme;},colorScale:getColorScale,aspectRatio:5,scale:0.7,quality:"custom",subdiv:function(){if(quality==="auto"){if(atomCount<15000){return 12;}else if(atomCount<70000){return 6;}else{return 3;}}else{if(quality==="high"){return 12;}else if(quality==="medium"){return 6;}else{return 3;}}},radialSegments:function(){if(quality==="auto"){if(atomCount<15000){return 20;}else if(atomCount<70000){return 10;}else{return 6;}}else{if(quality==="high"){return 20;}else if(quality==="medium"){return 10;}else{return 6;}}},sele:function(){var sele="";if(model!=="all"){sele+="/"+model;}
return sele;}},"base":{colorScheme:function(){return colorScheme;},colorScale:getColorScale,quality:"custom",sphereDetail:function(){if(quality==="auto"){return atomCount<15000?1:0;}else{if(quality==="high"){return 1;}else if(quality==="medium"){return 1;}else{return 0;}}},radialSegments:function(){if(quality==="auto"){if(atomCount<15000){return 20;}else if(atomCount<70000){return 10;}else{return 5;}}else{if(quality==="high"){return 20;}else if(quality==="medium"){return 10;}else{return 5;}}},sele:function(){var sele="polymer";if(model!=="all"){sele+=" and /"+model;}
return sele;}},"backbone":{lineOnly:function(){if(quality==="auto"){return atomCount>250000;}else{return quality==="low";}},colorScheme:function(){return colorScheme;},colorScale:getColorScale,scale:2.0,sele:function(){var sele="";if(model!=="all"){sele+="/"+model;}
return sele;}},"surface":{colorScheme:function(){return colorScheme;},colorScale:getColorScale,surfaceType:"sas",probeRadius:1.4,useWorker:true,scaleFactor:function(){var sf;if(quality==="low"){sf=0.1;}else if(quality==="medium"){sf=0.7;}else if(quality==="high"){sf=1.7;}else{sf=Math.min(1.5,Math.max(0.1,50000/atomCount));}
return sf;},sele:function(){var sele="polymer";if(model!=="all"){sele+=" and /"+model;}
if(hydrogenVisibility===false){sele+=" and not hydrogen";}
return sele;}},"spacefill":{colorScheme:function(){return colorScheme;},colorScale:getColorScale,quality:"custom",sphereDetail:function(){if(quality==="auto"){return atomCount<15000?1:0;}else{if(quality==="high"){return 1;}else if(quality==="medium"){return 1;}else{return 0;}}},sele:function(){var sele="polymer";if(model!=="all"){sele+=" and /"+model;}
if(hydrogenVisibility===false){sele+=" and not hydrogen";}
return sele;}},"licorice":{colorScheme:function(){return colorScheme;},colorScale:getColorScale,quality:"custom",sphereDetail:function(){if(quality==="auto"){return atomCount<15000?1:0;}else{if(quality==="high"){return 1;}else if(quality==="medium"){return 1;}else{return 0;}}},radialSegments:function(){if(quality==="auto"){if(atomCount<15000){return 20;}else if(atomCount<70000){return 10;}else{return 5;}}else{if(quality==="high"){return 20;}else if(quality==="medium"){return 10;}else{return 5;}}},sele:function(){var sele="polymer";if(model!=="all"){sele+=" and /"+model;}
if(hydrogenVisibility===false){sele+=" and not hydrogen";}
return sele;}}};var ligandReprDict={};var ligandReprDefs={"spacefill":{colorScheme:function(){if(colorScheme==="bfactor"){return colorScheme}else{return"element";}},quality:function(){return"medium";},sele:function(){var sele="not polymer";if(model!=="all"){sele+=" and /"+model;}
if(hydrogenVisibility===false){sele+=" and not hydrogen";}
if(ionVisibility===false){sele+=" and not ion";}
if(waterVisibility===false){sele+=" and not water";}
return sele;}},"ball+stick":{colorScheme:function(){if(colorScheme==="bfactor"){return colorScheme}else{return"element";}},quality:function(){return"medium";},scale:2.5,aspectRatio:1.2,sele:function(){var sele="not polymer";if(model!=="all"){sele+=" and /"+model;}
if(hydrogenVisibility===false){sele+=" and not hydrogen";}
if(ionVisibility===false){sele+=" and not ion";}
if(waterVisibility===false){sele+=" and not water";}
return sele;}}};function evalParam(paramValue){if(typeof paramValue==="function"){return paramValue();}else{return paramValue;}}
function getPolymerParam(reprName,paramName){return evalParam(polymerReprDefs[reprName][paramName]);}
function getLigandParam(reprName,paramName){return evalParam(ligandReprDefs[reprName][paramName]);}
function makeRepresentations(reprDefs,reprDict){if(!structureComponent)return;for(var reprName in reprDefs){var reprParams=reprDefs[reprName];var params={lazy:true,visible:false,assembly:assembly};for(var paramName in reprParams){params[paramName]=evalParam(reprParams[paramName]);}
if(reprDict[reprName]){reprDict[reprName].dispose();}
reprDict[reprName]=structureComponent.addRepresentation(reprName,params);}}
function makeCounts(){var structure=structureComponent.structure;var _assembly=structure.biomolDict[assembly];if(_assembly){atomCount=_assembly.getAtomCount(structure)
if(model!=="all"){atomCount/=structure.modelStore.count;}
instanceCount=_assembly.getInstanceCount();}else{if(model==="all"){atomCount=structure.atomStore.count;}else{atomCount=structure.getModelProxy(0).atomCount;}
instanceCount=1;}
if(typeof window.orientation!=='undefined'){atomCount*=4;}
isBackboneOnly=structure.atomStore.count/structure.residueStore.count<2;if(isBackboneOnly){atomCount*=10;}
console.log("atomCount",atomCount,"instanceCount",instanceCount);}
function setStructure(comp){structureComponent=comp;initStructure();signals.structureChanged.dispatch(structureComponent);}
function initStructure(){if(!structureComponent)return;makeCounts();if(getStyleNames(true)[style]===undefined){style=getDefaultStyle();}
if(getSymmetryNames()[symmetry]===undefined){symmetry=0;}
if(getSymmetryInfo()===undefined){loadSymmetryData(assembly).then(updateSymmetry);}
setSymmetry(symmetry);makeRepresentations(polymerReprDefs,polymerReprDict);makeRepresentations(ligandReprDefs,ligandReprDict);structureComponent.setDefaultAssembly(assembly);axesRepr=structureComponent.addRepresentation("axes",{visible:false});setStyle(style);setLigandStyle(ligandStyle);if(assembly==="UNITCELL"){polymerReprDict["unitcell"].setVisibility(true);}else if(assembly==="SUPERCELL"){setLigandStyle("");}else{axesRepr.repr.align();}
centerView();}
function loadPdbid(_pdbid,_assembly,_reduced){pdbid=_pdbid;symmetryData={};if(symmetryBuffer){symmetryBuffer.dispose();symmetryBuffer=undefined;}
if(_assembly!==undefined){assembly=_assembly;}
var mmtfUrl="rcsb://"+pdbid+(_reduced?".bb":"")+".mmtf";var mmcifUrl="rcsb://"+pdbid+".cif";var params={assembly:assembly,defaultRepresentation:false};return stage.loadFile(mmtfUrl,params).then(setStructure).catch(function(e){console.error(e);return stage.loadFile(mmcifUrl,params).then(setStructure).catch(function(e){console.error(e);});});}
function loadSymmetryData(_assembly){tasks.increment();return retrieveSymmetryData(pdbid,_assembly).then(function(data){tasks.decrement();if(!data||!data.symmetries||!data.symmetries.length){symmetry=-1;}else{data.symmetries=data.symmetries.filter(function(sym){return sym.pointGroup!=="C1";});if(!data.symmetries.length){symmetry=-1;}}
symmetryData[_assembly]=data;signals.symmetryDataLoaded.dispatch(data);}).catch(function(e){tasks.decrement();console.error(e);});}
function updateSelections(){var name;for(name in polymerReprDict){polymerReprDict[name].setSelection(getPolymerParam(name,"sele"));}
for(name in ligandReprDict){ligandReprDict[name].setSelection(getLigandParam(name,"sele"));}}
function setStyle(value){style=value;for(var name in polymerReprDict){if(name==="unitcell"&&assembly==="UNITCELL"){polymerReprDict["unitcell"].setVisibility(true);}else if(name==="base"&&style==="cartoon"){polymerReprDict["base"].setVisibility(true);}else{polymerReprDict[name].setVisibility(name===style);}}
signals.styleChanged.dispatch(style);}
function setLigandStyle(value){ligandStyle=value;for(var name in ligandReprDict){ligandReprDict[name].setVisibility(name===ligandStyle);}
signals.ligandStyleChanged.dispatch(ligandStyle);}
function setColorScheme(value){colorScheme=value;for(var name in polymerReprDict){polymerReprDict[name].setParameters({colorScheme:getPolymerParam(name,"colorScheme"),colorScale:getPolymerParam(name,"colorScale")});}
for(var name in ligandReprDict){ligandReprDict[name].setParameters({colorScheme:getLigandParam(name,"colorScheme"),colorScale:getLigandParam(name,"colorScale")});}
signals.colorSchemeChanged.dispatch(colorScheme);}
function setModel(value){if(value!==model&&(model==="all"||value==="all")){model=value;initStructure();}else{model=value;updateSelections();}
signals.modelChanged.dispatch(model);}
function setHydrogenVisibility(value){hydrogenVisibility=value;updateSelections();signals.hydrogenVisibilityChanged.dispatch(hydrogenVisibility);}
function setIonVisibility(value){ionVisibility=value;updateSelections();signals.ionVisibilityChanged.dispatch(ionVisibility);}
function setWaterVisibility(value){waterVisibility=value;updateSelections();signals.waterVisibilityChanged.dispatch(waterVisibility);}
function setQuality(value){quality=value;console.log(quality)
polymerReprDict["surface"].setParameters({scaleFactor:getPolymerParam("surface","scaleFactor")});polymerReprDict["cartoon"].setParameters({subdiv:getPolymerParam("cartoon","subdiv"),radialSegments:getPolymerParam("cartoon","radialSegments")});polymerReprDict["backbone"].setParameters({lineOnly:getPolymerParam("backbone","lineOnly")});polymerReprDict["spacefill"].setParameters({sphereDetail:getPolymerParam("spacefill","sphereDetail"),});signals.qualityChanged.dispatch(quality);}
function getDefaultStyle(){if(atomCount<100000){return"cartoon";}else if(atomCount<1000000){return"backbone";}else{return"surface";}}
function getColorScale(){console.log(colorScheme)
if(colorScheme==="hydrophobicity"){return"RdYlGn";}else if(colorScheme==="bfactor"){return"OrRd";}else{return"RdYlBu";}}
function setAssembly(value){assembly=value;initStructure();signals.assemblyChanged.dispatch(assembly);}
function setSpin(value){spin=value;if(spin===true){stage.setSpin([0,1,0],0.005);}else if(value===false){stage.setSpin(null,null);}}
function getSymmetryInfo(){var data=symmetryData[assembly];if(data&&data.nrSymmetries){return data.symmetries[symmetry];}else{return undefined;}}
function updateSymmetry(){if(symmetryBuffer){symmetryBuffer.dispose();symmetryBuffer=undefined;}
var data=getSymmetryInfo();if(data&&data.symmetryAxes){symmetryBuffer=new SymmetryBuffer(data.symmetryAxes,{});symmetryBuffer.attach(structureComponent);}
if(data&&data.rotation&&data.center){var r=data.rotation;var m3=new NGL.Matrix3().set(parseFloat(r.m00),parseFloat(r.m01),parseFloat(r.m02),parseFloat(r.m10),parseFloat(r.m11),parseFloat(r.m12),parseFloat(r.m20),parseFloat(r.m21),parseFloat(r.m22));var c=new NGL.Vector3().copy(data.center);var v1=new NGL.Vector3(parseFloat(r.m00),parseFloat(r.m01),parseFloat(r.m02));var v2=new NGL.Vector3(parseFloat(r.m10),parseFloat(r.m11),parseFloat(r.m12));var v3=new NGL.Vector3(parseFloat(r.m20),parseFloat(r.m21),parseFloat(r.m22));stage.viewer.alignView(v3,v1,c,false);stage.viewer.centerView(true);}}
function setSymmetry(value){symmetry=parseInt(value)||0;var data=getSymmetryInfo();if(symmetry===-1){if(symmetryBuffer){symmetryBuffer.dispose();symmetryBuffer=undefined;}}else if(data===undefined){if(symmetryBuffer){symmetryBuffer.dispose();symmetryBuffer=undefined;}
loadSymmetryData(assembly).then(updateSymmetry);}else{updateSymmetry();}
signals.symmetryChanged.dispatch(symmetry);}
function centerView(){stage.centerView();}
function downloadScreenshot(){stage.makeImage({factor:2,antialias:true,trim:false,transparent:false}).then(function(blob){NGL.download(blob,pdbid+"_screenshot.png");});}
function toggleFullscreen(element){stage.toggleFullscreen(element);}
function getStyleNames(recommended){var styleDict={"":"None",backbone:"Backbone",surface:"Surface",};if(recommended){if(atomCount<100000){styleDict["cartoon"]="Cartoon";}
if(atomCount<80000){styleDict["spacefill"]="Spacefill";}
if(atomCount<80000){styleDict["licorice"]="Licorice";}}else{styleDict["cartoon"]="Cartoon";if(!isBackboneOnly){styleDict["spacefill"]="Spacefill";styleDict["licorice"]="Licorice";}}
return styleDict;}
function getLigandStyleNames(){return{"":"None","ball+stick":"Ball & Stick",spacefill:"Spacefill"};}
function getModelNames(){var modelDict={};if(structureComponent){var modelStore=structureComponent.structure.modelStore;if(modelStore.count>1){modelDict["all"]="All Models";}
for(var i=0;i<modelStore.count;++i){modelDict[i]="Model "+(i+1);}}
return modelDict;}
function getAssemblyNames(){var assemblyDict={};if(structureComponent){var structure=structureComponent.structure;var biomolDict=structure.biomolDict;if(!structure.unitcell&&Object.keys(biomolDict).length===1&&biomolDict["BU1"]&&biomolDict["BU1"].isIdentity(structure)){assemblyDict["BU1"]="Full Structure";}else{assemblyDict["__AU"]=(structure.unitcell?"Asymmetric Unit":"Full Structure");for(var name in biomolDict){if(name==="UNITCELL"){assemblyDict[name]="Unitcell";}else if(name==="SUPERCELL"){assemblyDict[name]="Supercell";}else if(name.substr(0,2)==="BU"){assemblyDict[name]="Bioassembly "+name.substr(2);}else{assemblyDict[name]=name;}}}}
return assemblyDict;}
function getColorSchemeNames(){return{chainname:"By Chain",residueindex:"Rainbow",element:"By Element",bfactor:"By B-factor",sstruc:"By Secondary Structure",hydrophobicity:"By Hydrophobicity"};}
function getSymmetryNames(){var symmetryDict={"-1":"None"};var data=symmetryData[assembly];if(data&&data.symmetries){for(var i=0;i<data.symmetries.length;++i){var sym=data.symmetries[i];var type=sym.local?"local":"global";if(sym.pseudoSymmetric){type+=", pseudo";}
symmetryDict[i]=sym.pointGroup+" ("+type+")";}}
return symmetryDict;}
this.signals=signals;this.loadPdbid=loadPdbid;this.centerView=centerView;this.downloadScreenshot=downloadScreenshot;this.toggleFullscreen=toggleFullscreen;this.setStyle=setStyle;this.setLigandStyle=setLigandStyle;this.setModel=setModel;this.setHydrogenVisibility=setHydrogenVisibility;this.setIonVisibility=setIonVisibility;this.setWaterVisibility=setWaterVisibility;this.setQuality=setQuality;this.setAssembly=setAssembly;this.setColorScheme=setColorScheme;this.setSpin=setSpin;this.setSymmetry=setSymmetry;this.getStyle=function(){return style;};this.getLigandStyle=function(){return ligandStyle;};this.getModel=function(){return model;};this.getHydrogenVisibility=function(){return hydrogenVisibility;};this.getIonVisibility=function(){return ionVisibility;};this.getWaterVisibility=function(){return waterVisibility;};this.getQuality=function(){return quality;};this.getAssembly=function(){return assembly;};this.getSymmetry=function(){return symmetry;};this.getColorScheme=function(){return colorScheme;};this.getSpin=function(){return spin;};this.getStyleNames=getStyleNames;this.getLigandStyleNames=getLigandStyleNames;this.getModelNames=getModelNames;this.getAssemblyNames=getAssemblyNames;this.getColorSchemeNames=getColorSchemeNames;this.getSymmetryNames=getSymmetryNames;};