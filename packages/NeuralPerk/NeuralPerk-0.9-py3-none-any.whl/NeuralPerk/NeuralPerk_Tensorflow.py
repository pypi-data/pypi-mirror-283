from . import *

class ChooseOptionWindow(QMainWindow):
    def __init__(self, options):
        super().__init__()

        self.setWindowTitle("TRAINED MODELS")
        self.setMinimumSize(400, 300)

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        vbox = QVBoxLayout(central_widget)

        label = QLabel("Select a Model to Load:", self)
        label.setStyleSheet("font-size: 20px; color: #333; margin-bottom: 20px;")
        vbox.addWidget(label, alignment=Qt.AlignCenter)  # Align label to center

        self.list_widget = QListWidget(self)
        self.list_widget.addItems(options)
        self.list_widget.setStyleSheet("font-size: 16px; background-color: #f0f0f0;")
        vbox.addWidget(self.list_widget)

        hbox = QHBoxLayout()

        self.ok_button = QPushButton("OK", self)
        self.ok_button.setStyleSheet("font-size: 16px; background-color: #4CAF50; color: white; padding: 10px 20px; border: none;")
        self.ok_button.clicked.connect(self.on_ok_button_click)
        hbox.addWidget(self.ok_button)

        self.cancel_button = QPushButton("Cancel", self)
        self.cancel_button.setStyleSheet("font-size: 16px; background-color: #FF5722; color: white; padding: 10px 20px; border: none;")
        self.cancel_button.clicked.connect(self.on_cancel_button_click)
        hbox.addWidget(self.cancel_button)

        vbox.addLayout(hbox)
        vbox.addStretch(1)  # Add stretch to push widgets upwards

        self.final_selection = None

    def on_ok_button_click(self):
        selected_items = self.list_widget.selectedItems()
        if not selected_items:
            QMessageBox.warning(self, "No Selection", "Please select a model before clicking OK.")
        else:
            self.final_selection = selected_items[0].text()
            self.close()

    def on_cancel_button_click(self):
        self.final_selection = None
        self.close()



class Tensorflow_Manager():
    def __init__(self) -> None:
        self._connectedToServer = False
        self._sessionCreated = False
        self.allConfigsDone = False
        self.modelJson = None       # model.to_json()  
        self.modelWeights = None    # model.get_weights()
        self.optimizerConfig = None # model.optimizer.get_config()
        self.metricsList = None     # model.compiled_metrics._user_metrics
        self.loss = None            # model.compiled_loss._user_losses
        self.lossWeights = None     # model.compiled_loss._user_loss_weights
        self.weightedMetrics = None # model.compiled_metrics._user_weighted_metrics
        
        self.epoch = None
        self.callbackList = None    # Every Element of the List would be the list in itsself where the first index would represent type of Callback Function
                                    # abd rest would represent its configuration params
                                    # Callback Name : type(callback_var).__name__
                                    # Params : callback_var.paramName


    def checkConnectionAndCredentials(self):
        credentialServer_ipAddress = input("Enter the IP Address of the Server : ")  

        connectedToServer = False

        email , password = None , None

        try:
            requestURL = f"http://{credentialServer_ipAddress}:5500/serverRunning"
            response = requests.get(requestURL)
            if response.status_code == 200:
                data = response.json()
                if data['message'] == "Running":
                    print()
                    print("YOU HAVE CONNECTED TO THE SERVER !!")
                    print()
                    connectedToServer = True

                    email = input("Enter Your Account Email Address : ")
                    password = input("Enter Your Account Password : ")
                    jsMsg = json.dumps({"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password})
                    requestURL = f"http://{credentialServer_ipAddress}:5555/credentials?message={jsMsg}"

                    try:
                        response = requests.get(requestURL)

                        if response.status_code == 200:
                            if(response.json()['message'] == "VERIFIED"):
                                print()
                                print("CREDENTIALS VERIFIED !!")
                                print()
                                credentialsVerified = True
                            else:
                                print()
                                print("INVALID EMAIL OR PASSWORD !!")
                                print("--------------------------------------------------------------------------------------------------\n")
                                credentialsVerified = False
                                return [False , None]
                        else:
                            print()
                            print("INVALID EMAIL OR PASSWORD !!")
                            print("--------------------------------------------------------------------------------------------------\n")
                            credentialsVerified = False
                            return [False , None]
                    except Exception as error:
                        print()
                        print(f"THE FOLLOWING ERROR OCCURED WHEN VERIFING THE CREDENTIALS : {error}")
                        print("--------------------------------------------------------------------------------------------------\n")
                        credentialsVerified = False
                        return [False , None]

                else:
                    print("SERVER IS NOT RUNNING RIGHT NOW !!!")
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    connectedToServer = False
                    return [False , None]
        except requests.exceptions.ConnectionError:
            print("EITHER SERVER IS NOT RUNNING RIGHT NOW OR THE IP ADDRESS ENTERED IS INCORRECT\nPLEASE CHECK THE ENTERED IP ADDRESS OR ELSE TRY AGAIN LATER")
            print("\n--------------------------------------------------------------------------------------------------\n")
            connectedToServer = False
            return 
        except Exception as error:
            print(f"THE FOLLOWING ERROR OCCURED WHEN CONNECTING TO THE SERVER : {error}")
            print("\n--------------------------------------------------------------------------------------------------\n")
            credentialsVerified = False
            return [False , None]

        if(not connectedToServer):
            print("YOUR ARE NOT CONNECTED TO THE SERVER !!")
            print("PLEASE CONNECT TO THE SERVER FIRST !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return [False , None]
        
        return [True,[credentialServer_ipAddress , email , password]]

    def initiateSessionRequest(self):
        # print("\n--------------------------------------------------------------------------------------------------\n")

        # if self.allConfigsDone == False:
        #     print("PLEASE CONFIGURE THE MODEL FIRST !!")
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        #     return
        
        # credentialServer_ipAddress = input("Enter the IP Address of the Server : ")  

        # connectedToServer = False

        # email , password = None , None

        # try:
        #     requestURL = f"http://{credentialServer_ipAddress}:5500/serverRunning"
        #     response = requests.get(requestURL)
        #     if response.status_code == 200:
        #         data = response.json()
        #         if data['message'] == "Running":
        #             print()
        #             print("YOU HAVE CONNECTED TO THE SERVER !!")
        #             print()
        #             connectedToServer = True

        #             email = input("Enter Your Account Email Address : ")
        #             password = input("Enter Your Account Password : ")
        #             jsMsg = json.dumps({"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password})
        #             requestURL = f"http://{credentialServer_ipAddress}:5555/credentials?message={jsMsg}"

        #             try:
        #                 response = requests.get(requestURL)

        #                 if response.status_code == 200:
        #                     if(response.json()['message'] == "VERIFIED"):
        #                         print()
        #                         print("CREDENTIALS VERIFIED !!")
        #                         print()
        #                         credentialsVerified = True
        #                     else:
        #                         print()
        #                         print("INVALID EMAIL OR PASSWORD !!")
        #                         print("--------------------------------------------------------------------------------------------------\n")
        #                         credentialsVerified = False
        #                         return
        #                 else:
        #                     print()
        #                     print("INVALID EMAIL OR PASSWORD !!")
        #                     print("--------------------------------------------------------------------------------------------------\n")
        #                     credentialsVerified = False
        #                     return
        #             except Exception as error:
        #                 print()
        #                 print(f"THE FOLLOWING ERROR OCCURED WHEN VERIFING THE CREDENTIALS : {error}")
        #                 print("--------------------------------------------------------------------------------------------------\n")
        #                 credentialsVerified = False
        #                 return

        #         else:
        #             print("SERVER IS NOT RUNNING RIGHT NOW !!!")
        #             print("\n--------------------------------------------------------------------------------------------------\n")
        #             connectedToServer = False
        #             return 
        # except requests.exceptions.ConnectionError:
        #     print("EITHER SERVER IS NOT RUNNING RIGHT NOW OR THE IP ADDRESS ENTERED IS INCORRECT\nPLEASE CHECK THE ENTERED IP ADDRESS OR ELSE TRY AGAIN LATER")
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        #     connectedToServer = False
        #     return 
        # except Exception as error:
        #     print(f"THE FOLLOWING ERROR OCCURED WHEN CONNECTING TO THE SERVER : {error}")
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        #     credentialsVerified = False
        #     return 

        # if(not connectedToServer):
        #     print("YOUR ARE NOT CONNECTED TO THE SERVER !!")
        #     print("PLEASE CONNECT TO THE SERVER FIRST !!")
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        #     return

        
        print("\n--------------------------------------------------------------------------------------------------\n")

        if self.allConfigsDone == False:
            print("PLEASE CONFIGURE THE MODEL FIRST !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return

        isSuccess , data = self.checkConnectionAndCredentials()
        if isSuccess == False:
            return
        
        credentialServer_ipAddress , email , password = data
        
        try:
            # email = input("Enter Your Account Email Address : ")
            # password = input("Enter Your Account Password : ")

            self.optimizerConfig["config"]["learning_rate"] = float(self.optimizerConfig["config"]["learning_rate"])

            relevantInformation = {"MODEL_JSON" : self.modelJson , "MODEL_WEIGHTS" : self.modelWeights , "OPTIMIZER_CONFIG" : self.optimizerConfig , "METRICS" : self.metricsList , "LOSS" : self.loss , "LOSS_WEIGHTS" : self.lossWeights , "WEIGHTED_METRICS" : self.weightedMetrics , "EPOCHS" : self.epoch}
            jsMsg = {"TYPE" : "CUSTOMERS" , "EMAIL" : email , "PASSWORD" : password , "DATA" : relevantInformation}
            requestURL = f"http://{credentialServer_ipAddress}:5500/requestSessionCreation"
            response = requests.post(requestURL , data=pickle.dumps(jsMsg) , headers={'content-type': 'application/bytes'})
            if response.status_code == 200:
                data = response.json()
                if data['message'] == "Request Submitted":
                    print("THE REQUEST WAS SUBMITTED SUCCESSFULLY !!")
                    print("INITIALIZE YOU SESSION USING YOUR DESKTOP APPLICATION !!")
                    self._sessionCreated = True
                    self._connectedToServer = True
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    return
                else:
                    print(data['message'])
                    print("\n--------------------------------------------------------------------------------------------------\n")
                    return 
            else:
                print("SESSION COULD NOT BE CREATED !!")
                print(response.json()['message'])
                print("\n--------------------------------------------------------------------------------------------------\n")
                return 
        except Exception as error:
            print(f"THE FOLLOWING ERROR OCCURED WHEN CREATING THE SESSION : {error}")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return
        


    def InformationTransfer(self , model , epochs):
        self.setModel(model)
        self.setEpochs(epochs)
        pass

    def setEpochs(self , epochs):
        if type(epochs) == int:
            self.epoch = epochs
        else:
            print("\n--------------------------------------------------------------------------------------------------\n")
            print("PLEASE ENTER A VALID INTEGER VALUE FOR EPOCHS !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
    

    def setModel(self , model):

        try:
            self.modelJson = model.to_json()
        except Exception as error:
            print("\n--------------------------------------------------------------------------------------------------\n")    
            print("Invalid Model !!")
            print("The Given object cannot be converted to into the format that can be used to Transmit it Further !!")
            print("Pls Check That you have passed an object Belonging the Following Classes : \n<class 'keras.engine.functional.Functional'> \n<class 'keras.engine.sequential.Sequential'>")
            print("\n--------------------------------------------------------------------------------------------------\n")

            return
        
        try:
            checkModel = keras.models.model_from_json(self.modelJson)
        except Exception as error:
            print("\n--------------------------------------------------------------------------------------------------\n")    
            print("Invalid Model !!")
            print("Pls Check Again the Model Layers and that the Correct Model Object is being passed !!")
            print("\n--------------------------------------------------------------------------------------------------\n")
            return

        self.modelJson = json.loads(self.modelJson)
        self.modelWeights = model.get_weights() 
        
        print("\n--------------------------------------------------------------------------------------------------\n")
        print("MODEL CONFIGURATIONS HAS BEEN SUCCESSFULLY NOTED DOWN !!")


        if not model.optimizer:
                print("MODEL HAS NO OPTIMIZER")
                print("PLEASE COMPILE THE MODEL BEFORE SENDING THE MODEL")
                print("\n--------------------------------------------------------------------------------------------------\n")
                return
        self.setOptimizer(model.optimizer)
        self.setLoss(model.compiled_loss._user_losses)
        self.setMetrics(model.compiled_metrics._user_metrics)
        self.setLossWeights(model.compiled_loss._user_loss_weights)
        self.setWeightedMetrics(model.compiled_metrics._user_weighted_metrics)
        self.allConfigsDone = True
        print("MODEL OPTIMIZER IS ALSO SUCCESSFULLY NOTED DOWN !!")
        print("\n--------------------------------------------------------------------------------------------------\n")
        return
    

        # if isinstance(model, keras_models.Sequential) or isinstance(model, keras_models.Model):
        #     self.modelJson = json.loads(model.to_json())
        #     if self.validModelLayers(model.layers) == False:
        #         print("\n--------------------------------------------------------------------------------------------------\n")
        #         print("INVALID MODEL LAYERS GIVEN !!")
        #         print("\n--------------------------------------------------------------------------------------------------\n")
        #         self.allConfigsDone = False
        #         modelJson = None
        #         return 
        #     else:
        #         print("\n--------------------------------------------------------------------------------------------------\n")
        #         print("MODEL CONFIGURATIONS HAS BEEN SUCCESSFULLY NOTED DOWN !!")

        #     if not model.optimizer:
        #         print("MODEL HAS NO OPTIMIZER")
        #         print("PLEASE COMPILE THE MODEL BEFORE SENDING THE MODEL")
        #         print("\n--------------------------------------------------------------------------------------------------\n")
        #         return
        #     self.setOptimizer(model.optimizer)
        #     self.setLoss(model.compiled_loss._user_losses)
        #     self.setMetrics(model.compiled_metrics._user_metrics)
        #     self.setLossWeights(model.compiled_loss._user_loss_weights)
        #     self.setWeightedMetrics(model.compiled_metrics._user_weighted_metrics)
        #     self.allConfigsDone = True
        #     print("MODEL OPTIMIZER IS ALSO SUCCESSFULLY NOTED DOWN !!")
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        # else:
        #     print("\n--------------------------------------------------------------------------------------------------\n")
        #     print("PASS A VALID MODEL")
        #     print("\n--------------------------------------------------------------------------------------------------\n")

    def setOptimizer(self , optimizer):
        if optimizer:
            self.optimizerConfig = keras.optimizers.serialize(optimizer)
        
    def setLoss(self , loss):
        self.loss = loss
    
    def setMetrics(self , metrics):
        self.metricsList = metrics
    
    def setLossWeights(self , lossWeights):
        self.lossWeights = lossWeights
    
    def setWeightedMetrics(self , weightedMetrics):
        self.weightedMetrics = weightedMetrics

    def AllConfigs(self):
        print("Model Json : " , self.modelJson)
        print("Optimizer Config : " , self.optimizerConfig)
        print("Loss : " , self.loss)
        print("Metrics : " , self.metricsList)
        print("Loss Weights : " , self.lossWeights)
        print("Weighted Metrics : " , self.weightedMetrics)
        print("Epochs : " , self.epoch)
    

    def choose_option(self , options):
        app = QApplication(sys.argv)
        window = ChooseOptionWindow(options)

        # Apply overall stylesheet to QMainWindow
        window.setStyleSheet("""
            QMainWindow {
                background-color: #ffffff;
            }
            QLabel {
                font-size: 20px;
                color: #333333;
            }
            QListWidget {
                font-size: 16px;
                background-color: #f0f0f0;
            }
            QPushButton {
                font-size: 16px;
                padding: 10px 20px;
                border: none;
            }
            QPushButton#okButton {
                background-color: #4CAF50;
                color: white;
            }
            QPushButton#cancelButton {
                background-color: #FF5722;
                color: white;
            }
        """)

        window.show()
        app.exec_()
        return window.final_selection

    def loadModel(self):
        print("\n--------------------------------------------------------------------------------------------------\n")
        
        isSuccess , data = self.checkConnectionAndCredentials()
        if isSuccess == False:
            return
        
        credentialServer_ipAddress , email , password = data

        jsMsg = json.dumps({"TYPE" : "GET_TRAINED_MODELS" , "EMAIL" : email})
        response = requests.get(f'http://{credentialServer_ipAddress}:5555/getCustomerData?message={jsMsg}')
        options = []
        if response.status_code == 200:
            options = response.json()['DATA']
        
        final_model_selection = self.choose_option(options)
        print("FINAL MODEL SELECTION : " , final_model_selection)

        if final_model_selection == None:
            print("\n--------------------------------------------------------------------------------------------------\n")
            return
        
        jsMsg = json.dumps({"TYPE" : "GET_MODEL" , "EMAIL" : email , "MODEL_NAME" : final_model_selection})
        response = requests.get(f'http://127.0.0.1:5555/getCustomerData?message={jsMsg}')
        data = pickle.loads(response.content)
        statuscode = response.status_code

        print(type(data["MODEL_CONFIG"]))
        print(len(pickle.dumps(data)))

        model = None
        if statuscode == 200:
            model = keras.models.model_from_json(data['MODEL_CONFIG'])
            model.set_weights(data['MODEL_WEIGHTS'])
        else:
            print("MODEL COULD NOT BE LOADED !!")

        print("\n--------------------------------------------------------------------------------------------------\n")
        return model

        

