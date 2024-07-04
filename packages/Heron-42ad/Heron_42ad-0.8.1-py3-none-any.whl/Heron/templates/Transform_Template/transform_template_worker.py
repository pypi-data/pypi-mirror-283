
# This is the code of the worker part of the Transform Operation. Here the user needs to write most of the code in
# order to define the Operation's functionality.

# <editor-fold desc="The following 6 lines of code are required to allow Heron to be able to see the Operation without
# package installation. Do not change.">
import sys
from os import path
from typing import List, Union
import numpy as np

current_dir = path.dirname(path.abspath(__file__))
while path.split(current_dir)[-1] != r'Heron':
    current_dir = path.dirname(current_dir)
sys.path.insert(0, path.dirname(current_dir))
# </editor-fold>

# <editor-fold desc="Extra imports if required">
from Heron.communication.socket_for_serialization import Socket
from Heron import general_utils as gu, constants as ct
from Heron.gui.visualisation_dpg import VisualisationDPG
from Heron.communication.transform_worker import TransformWorker
# </editor-fold>

# <editor-fold desc="Global variables if required. Global variables operate obviously within the scope of the process
# that is running when this script is called so they pose no existential threats and are very useful in keeping state
# over different calls of the work function (see below).">
need_parameters = True
global_var_1: str
global_var_2: str
global_var_3: float
global_var_4: int

# The following global is useful if you need a updatable visualisation window in the Node
vis: VisualisationDPG
# </editor-fold>


# The initialise function is called when the worker process is fired up from the com process and it keeps getting called
# as long as it is returning False. The worker object will not pass data to the work_function of this script (here is
# the transform function) unless the initialise has returned True. It gets passed the worker_object which carries the
# parameters from the GUI so, it is used to initialise the parameters values in the worker process (and of course for
# any other initialisation required, e.g. initialising a driver or starting a thread). Here is also where the
# initialisation of the Visualisation object needs to happen because it needs the Node's name and index that are
# carried in the worker object
def initialise(worker_object: TransformWorker) -> bool:
    global vis

    global global_var_1
    global global_var_2
    global global_var_3
    global global_var_4

    # INITIALISE PARAMETERS
    # Put the initialisation of the Node's parameter's in a try loop to take care of the time it takes for the GUI to
    # update the SinkWorker object.
    try:
        parameters = worker_object.parameters
        global_var_1 = parameters[1]
        global_var_2 = parameters[2]
        global_var_3 = parameters[3]
        global_var_4 = parameters[4]
    except:
        return False

    # VISUALISATION
    # The following three lines are required if you want visualisation from the Node itself. There are currently four
    # visualisation types ('Image', 'Value', 'Single Pane Plot', 'Multi Pane Plot') you can choose from. See the
    # gui.visualisation_dpg.VisualisationDPG class.
    visualisation_type = 'Value'
    buffer = 20
    vis = VisualisationDPG(_node_name=worker_object.node_name, _node_index=worker_object.node_index,
                           _visualisation_type=visualisation_type, _buffer=buffer)

    # SAVE STATE
    # If you want the possibility to save the parameters as you update them live during a Graph running then add the
    # following line. The names, parameter_var_1, parameter_var_2, etc. will be the names of the columns in the saved
    # pandas dataframe.
    worker_object.savenodestate_create_parameters_df(parameter_var_1=global_var_1, parameter_var_2=global_var_2,
                                                     parameter_var_3=global_var_3, parameter_var_4=global_var_4)

    # Do other initialisation stuff
    return True


def work_function(data: List[Union[np.ndarray, dict]],
                  parameters: List,
                  savenodestate_update_substate_df: TransformWorker.savenodestate_update_substate_df) -> \
        List[Union[np.ndarray, dict]]:
    global vis
    global global_var_1
    global global_var_2
    global global_var_3
    global global_var_4

    '''
    # This is a 2nd way to initialise the parameters if no initialisation function is used.
    if need_parameters:
        try:
            global_var_1 = parameters[1]
            global_var_2 = parameters[2]
            global_var_3 = parameters[3]
            global_var_1 = parameters[4]

            need_parameters = True
        except:
            pass
    
    else:
        # Do the rest of the code in here so that it doesn't run if the parameters are not set
    '''

    # UPDATABLE PARAMETERS
    # If any parameters need to be updated during runtime then do that here, e.g.
    # Also update the visualisation parameter. This allows to turn on and off the visualisation window during
    # run time
    try:
        global_var_1 = parameters[1]

        vis.visualisation_on = parameters[0]
    except:
        pass

    # TOPICS FOR MULTIPLE INPUTS
    # In the case of multiple inputs the topic will tell you which input the message has come from. The topic is a
    # string that is formatted as follows:
    # previous_node_output_name##previous_node_name##previous_node_index -> this_node_input_name##this_none_name##this_node_index
    # so, you can see which input the data is coming from by looking at the this_node_input_name part. Also, although the
    # names of the inputs and outputs can have spaces, these become underscores in the names of the topics.
    topic = data[0]
    print(topic)  # prints will not work if the operation is running on a different computer.

    # GET THE DATA
    message = data[1:]  # data[0] is the topic
    # This is needed to reconstruct the message that comes in into the numpy array that it is.
    # Use Socket.reconstruct_data_from_bytes_message if the data is just a numpy array or a dictionary
    # or Socket.reconstruct_array_from_bytes_message_cv2correction if the data is an image (and the numpy array's type
    # needs to be unsigned
    message = Socket.reconstruct_data_from_bytes_message(message)

    # Now do stuff
    print(message.shape)
    some_data_to_visualise = message

    # SAVE TO SUBSTATE
    # Save something to the Substate. This is optional. If you do not use the save system to save some data then you
    # can define the work function as work_function(data, parameters) and not use the savenodestate_update_substate_df
    # parameter
    savenodestate_update_substate_df(image__shape=message.shape)

    # Whatever data the Node must visualise should be passed to the vis.visualise function
    vis.visualise(some_data_to_visualise)

    # For Operations with multiple outputs the work_function must return a list of numpy arrays with length the number
    # of outputs. Each array from left to right in the list gets passed to each output from top to bottom on the Node.
    # So in this example the data would go out of the 'Something Out 1' output and the np.array([ct.IGNORE]) would go
    # out of the 'Something Out 2' output. If you want to stop one or more outputs from sending out any data on the
    # current pass then put as an array the np.array([ct.IGNORE]) array. The com process knows to ignore this array.
    result = [message, np.array([ct.IGNORE])]

    return result


# The on_end_of_life function must exist even if it is just a pass
def on_end_of_life():
    global vis
    # If using in Node visualisation then the vis object must be cleared here like this
    vis.end_of_life()


if __name__ == "__main__":
    worker_object = gu.start_the_transform_worker_process(work_function=work_function,
                                                          end_of_life_function=on_end_of_life,
                                                          initialisation_function=initialise)
    worker_object.start_ioloop()
