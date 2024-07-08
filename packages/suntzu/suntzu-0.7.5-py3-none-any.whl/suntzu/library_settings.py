import os
import pandas as pd
import requests
import xarray as xr
import matplotlib.pyplot as plt
import pyarrow.parquet as pq
import json
import itertools
from matplotlib.container import BarContainer
import numpy as np
from slack_sdk import WebClient # type: ignore
from slack_sdk.errors import SlackApiError # type: ignore

from cycler import cycler
from .statistics import Statistics
from .cleaning import Cleaning
from .metadata import netCDFMetadata
from .metadata import ParquetMetadata
from .optimization import Optimization
from .visualization import Visualization
class Settings:
    @staticmethod
    def save_telegram_credentials(bot_token: str =None, chat_id: str=None):
        """
        Save the Telegram credentials to a JSON file.

        Args:
            bot_token (str, optional): The bot token. If not provided, the user will be prompted to enter it.
            chat_id (str, optional): The chat ID. If not provided, the user will be prompted to enter it.
            filename (str, optional): The name of the JSON file to save the credentials. Defaults to "telegram_credentials.json".
        """
        bot_token = bot_token or input("Insert the bot_token: ")
        chat_id = chat_id or input("Insert the chat id: ")
        dictionary = {"chat_id": chat_id, "bot_token": bot_token}
        try:
            with open('telegram_credentials.json', "w") as outfile:
                json.dump(dictionary, outfile)
        except Exception as e:
            print("Error occurred while saving telegram credentials:", str(e))
    @staticmethod
    def send_images_via_telegram(file_path: str, chat_id: str=None, bot_token: str =None, caption: str ="This is a caption"):
        """
        Sends an image via Telegram using the provided file path, chat ID, bot token, and caption.

        Args:
            file_path (str): The path to the image file.
            chat_id (str, optional): The ID of the chat to send the image to. If not provided, it will be retrieved from the 'telegram_credentials.json' file. Defaults to None.
            bot_token (str, optional): The token of the Telegram bot. If not provided, it will be retrieved from the 'telegram_credentials.json' file. Defaults to None.
            caption (str, optional): The caption for the image. Defaults to "This is a caption".

        Raises:
            ValueError: If chat_id and bot_token are not provided and the 'telegram_credentials.json' file does not exist.
            ValueError: If chat_id or bot_token is not provided.

        Returns:
            None
        """
        if chat_id is None and bot_token is None:
            if os.path.exists('telegram_credentials.json'):
                try:
                    with open('telegram_credentials.json', 'r') as openfile:
                        json_object = json.load(openfile)
                    chat_id = json_object.get("chat_id")
                    bot_token = json_object.get("bot_token")
                except ValueError:
                    print("Please use the function 'save_telegram_credentials'")
            else:
                raise ValueError("Please provide the chat_id and the bot_token or use the function 'save_telegram_credentials'.")
        if chat_id is None or bot_token is None:
            raise ValueError("chat_id and bot_token are required parameters")
        base_url = f"https://api.telegram.org/bot{bot_token}/sendPhoto"
        with open(file_path, 'rb') as my_file:
            parameters = {
                "chat_id": chat_id,
                "caption": caption
            }
            files = {   
                "photo": my_file
            }
            try:
                resp = requests.post(base_url, data=parameters, files=files)
                status_code = resp.status_code
                if status_code == 200:
                    print("The photo was sent.")
                else:
                    resp_json = resp.json()
                    print("Sent","-", resp_json.get("ok"))
                    del resp_json["ok"]
                    for key, values in resp_json.items():
                        print(key.capitalize(), "-", values)
            except requests.exceptions.RequestException as e:
                print("An error occurred during the request:", str(e))
    @staticmethod
    def help_telegram_bot():
        """
        Provides information on how to use a Telegram bot.
        """
        print('''
        1. How to create a bot: https://www.directual.com/lesson-library/how-to-create-a-telegram-bot
        2. Adding the bot to a group: https://botifi.me/en/help/telegram-adding-bot-to-channel-or-group/
        3. Getting the bot_token: https://botifi.me/en/help/telegram-existed-bot/
        4. Getting the chat_id of a group: https://www.wikihow.com/Know-Chat-ID-on-Telegram-on-Android
        5. Possible errors: https://core.telegram.org/api/errors
        ''')
    @staticmethod
    def save_slack_credentials(channel_id:str = None, slack_token:str=None):
        """
        Saves Slack credentials (channel ID and token) to a JSON file.

        Args:
            channel_id (str, optional): The ID of the Slack channel. If not provided, the user will be prompted to enter it.
            slack_token (str, optional): The Slack token. If not provided, the user will be prompted to enter it.

        Returns:
            None: The function does not return any value.
        """
        slack_token = slack_token or input("Insert the slack_token: ")
        channel_id = channel_id or input("Insert the channel_id: ")
        dictionary = {"channel_id": channel_id, "slack_token": slack_token}
        try:
            with open('slack_credentials.json', "w") as outfile:
                json.dump(dictionary, outfile)
        except Exception as e:
            print("Error occurred while saving slack credentials:", str(e))
    @staticmethod
    def send_images_via_slack(file_path: str, channel_id: str=None, slack_token: str =None, caption: str ="This is a caption"):
        """
        Sends an image file to a specified Slack channel using the Slack API.

        Args:
            file_path (str): The path to the image file to be sent.
            channel_id (str, optional): The ID of the Slack channel to send the image to. If not provided, it will attempt to read the channel ID from a JSON file named 'slack_credentials.json'.
            slack_token (str, optional): The Slack API token. If not provided, it will attempt to read the token from the same JSON file mentioned above.
            caption (str, optional): The caption to be displayed with the image in Slack.

        Raises:
            ValueError: If 'slack_credentials.json' file is not found or the values are not valid.
            ValueError: If either `channel_id` or `slack_token` is missing.

        Returns:
            None
        """
        if channel_id is None and slack_token is None:
            if os.path.exists('slack_credentials.json'):
                try:
                    with open('slack_credentials.json', 'r') as openfile:
                        json_object = json.load(openfile)
                    channel_id = json_object.get("channel_id")
                    slack_token = json_object.get("slack_token")
                except ValueError:
                    print("Please use the function 'save_slack_credentials'")
            else:
                raise ValueError("Please provide the channel_id and the slack_token or use the function 'save_slack_credentials'.")
        if channel_id is None or slack_token is None:
            raise ValueError("channel_id and slack_token are required parameters")
        client = WebClient(token=slack_token)
        try:
            response = client.files_upload(
                channels=channel_id,
                file=file_path,
                title=caption
            )
            if response["ok"]:
                print("The photo was sent.")
            else:
                for key, value in response.items():
                    print(f"{key.capitalize()}: {value}")
        except SlackApiError as e:
            print(f"Error uploading file: {e.response['error']}")
    @staticmethod
    def help_slack_bot():
        """
        Provides a list of resources to help users create and configure a Slack bot.
        """
        print('''
            1. Creating a slack_bot (read the first paragraph): https://medium.com/applied-data-science/how-to-build-you-own-slack-bot-714283fd16e5
            2. Getting the channel_id (read method 1): https://www.process.st/how-to/find-slack-channel-id/ 
            ''')
    @staticmethod
    def get_file_extension(path):
        """
        Returns the file extension of a given file path.

        Args:
            path (str): The file path.

        Returns:
            str: The file extension.
        """
        return os.path.splitext(path)[1]

    def export_to_file(self: pd.DataFrame | xr.Dataset, filename: str):
        """
        Exports data to a file with a specified filename.

        Args:
            filename (str): The name of the file to export the data to.

        Raises:
            ValueError: If the file extension is not valid.
            FileExistsError: If the file already exists.
        """
        # List of valid file extensions
        suffixs = [".nc", ".parquet"]
        # Check if the filename exists
        if not os.path.isfile(filename):
            # Check if the filename has a valid file extension
            if Settings.get_file_extension(filename) in suffixs:
                # If the file extension is .nc, convert it to netCDF
                if Settings.get_file_extension(filename) == ".nc":
                    self.to_netcdf(filename)
                # If the file extension is .parquet, convert it to parquet
                elif Settings.get_file_extension(filename) == ".parquet":
                    pq.write_table(self, filename, compression=None)        
            # Raise an error if the file extension is invalid
            else:
                raise ValueError(f"Invalid file extension. Please provide a valid filename. Valid file extesions {suffixs}.")
        # Raise an error if the file already exists
        else:
            raise FileExistsError(f"{filename} already exists. Please change it or delete it.")
    def increase_graph_size(width: int, height: int) -> None:
        """
        This function increases the size of the graph.

        Parameters:
        width (int): The width of the graph in inches.
        height (int): The height of the graph in inches.

        Returns:
        None
        """
        plt.rcParams['figure.figsize'] = (width, height)
    def set_grid(grid_backgroundcolor: str ="#EBEBEB", grid_border: list[bool] = [True, True, True, True], gridline: str ="white", gridlinewidth: int | float =1.2, minorgridlines: bool=False):
        """
        This function sets the grid properties of the plot.

        Parameters:
        grid_backgroundcolor (str): The background color of the grid. Default is "#EBEBEB".
        grid_border (list[bool]): A list of four boolean values indicating the visibility of the top, right, bottom, and left borders of the grid. Default is [True, True, True, True].
        gridline (str): The color of the grid lines. Default is "white".
        gridlinewidth (int | float): The width of the grid lines. Default is 1.2.
        minorgridlines (bool): A boolean indicating whether to display minor grid lines. Default is False.

        Returns:
        None
        """
        plt.rcParams['axes.facecolor'] = grid_backgroundcolor  
        plt.rcParams['axes.grid.axis'] = 'both'
        plt.rcParams['axes.grid.which'] = 'major'  
        plt.rcParams['grid.color'] = gridline  
        plt.rcParams['grid.linewidth'] = gridlinewidth 
        plt.rcParams['axes.grid'] = True
        plt.rcParams['axes.spines.top'] = grid_border[0]  
        plt.rcParams['axes.spines.right'] = grid_border[1]
        plt.rcParams['axes.spines.bottom'] = grid_border[2]  
        plt.rcParams['axes.spines.left'] = grid_border[3]
    def set_full_view(all_cols: bool=True, rows_fullsize: bool=True, max_rowswidth: bool = False, max_colwidth: bool=True):
        """
        This function sets the display options for pandas DataFrame to show all columns, all rows, maximum width, or maximum column width.

        Parameters:
        all_cols (bool): If True, it sets the maximum number of columns to be displayed. Default is True.
        rows_fullsize (bool): If True, it sets the maximum number of rows to be displayed. Default is True.
        max_rowswidth (bool): If True, it sets the maximum width of the rows to be displayed. Default is False.
        max_colwidth (bool): If True, it sets the maximum width of the columns to be displayed. Default is True.

        Returns:
        None
        """
        if rows_fullsize:
            pd.set_option('display.max_rows', None)
        elif all_cols:
            pd.set_option('display.max_columns', None)
        elif max_rowswidth:
            pd.set_option('display.width', None)
        elif max_colwidth:
            pd.set_option('display.max_colwidth', None)
    def reset_settings(matplotlib=True, pandas=True):
        """
        This function resets the settings of matplotlib and pandas to their default values.

        Parameters:
        matplotlib (bool): A boolean indicating whether to reset the matplotlib settings. Default is True.
        pandas (bool): A boolean indicating whether to reset the pandas settings. Default is True.

        Returns:
        None
        """
        if pandas:
            pd.reset_option('all')
        if matplotlib:
            plt.rcdefaults()
    def set_labels_settings(font: str= "serif",labelcolor: str = "black", labelsize: int | str = "medium", labelweight: str = "normal", pad: int |str= 4):
        """
        This function sets the label properties of the plot.

        Parameters:
        font (str): The font family for the labels. Default is "serif".
        labelcolor (str): The color of the labels. Default is "black".
        labelsize (int | str): The size of the labels. Default is "medium".
        labelweight (str): The weight of the labels. Default is "normal".
        pad (int | str): The padding around the labels. Default is 4.

        Returns:
        None
        """
        plt.rcParams['axes.labelcolor'] = labelcolor
        plt.rcParams['axes.labelsize'] = labelsize
        plt.rcParams['axes.labelweight'] = labelweight
        plt.rcParams['axes.labelpad'] = pad
        plt.rcParams['font.family'] = font
    def set_marker_settings(size: int | float = 10, type: str = 'o', color: str | list[str] = "green", outline: str = "white", outlinewidth: int | float = 1):
        """
        This function sets the marker properties for scatter plots.

        Parameters:
        size (int | float): The size of the marker. Default is 10.
        type (str): The type of the marker. Default is 'o'.
        color (str | list[str]): The color(s) of the marker. Default is "green".
        outline (str): The color of the marker outline. Default is "white".
        outlinewidth (int | float): The width of the marker outline. Default is 1.

        Returns:
        None
        """
        plt.rcParams['scatter.marker'] = type
        plt.rcParams['axes.prop_cycle'] = cycler('color', [color, '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf'])
        plt.rcParams['scatter.edgecolors'] = outline
        plt.rcParams['lines.linewidth'] = outlinewidth
        plt.rcParams['lines.markersize'] = size
    def set_title_settings(color: str = 'auto', location: str = 'center', size: int | str = 'large', weight: str = "bold", pad: int | float = 6.0) -> None:
        """
        This function sets the title properties of the plot.

        Parameters:
        color (str): The color of the title. Default is 'auto'.
        location (str): The location of the title. Default is 'center'.
        size (int | str): The size of the title. Default is 'large'.
        weight (str): The weight of the title. Default is 'bold'.
        pad (int | float): The padding around the title. Default is 6.0.

        Returns:
        None
        """
        plt.rcParams['axes.titlecolor'] = color
        plt.rcParams['axes.titlelocation'] = location
        plt.rcParams['axes.titlesize'] = size
        plt.rcParams['axes.titleweight'] = weight
        plt.rcParams['axes.titlepad'] = pad
    def set_line_settings(color: str = "green", linestyle: str ="-", linewidth: int | float = 1.5, marker: str = "None", markeredgecolor: str = 'auto', markeredgewidth: int | float = 1.0, markerfacecolor: str = 'auto', markersize: int | float = 6.0) -> None:
        """
        This function sets the line properties for plots.

        Parameters:
        color (str): The color of the line. Default is "green".
        linestyle (str): The style of the line. Default is "-".
        linewidth (int | float): The width of the line. Default is 1.5.
        marker (str): The marker style for data points. Default is "None".
        markeredgecolor (str): The color of the marker edge. Default is 'auto'.
        markeredgewidth (int | float): The width of the marker edge. Default is 1.0.
        markerfacecolor (str): The color of the marker face. Default is 'auto'.
        markersize (int | float): The size of the marker. Default is 6.0.

        Returns:
        None
        """
        plt.rcParams['lines.color'] = color
        plt.rcParams['lines.linestyle'] = linestyle
        plt.rcParams['lines.linewidth'] = linewidth
        plt.rcParams['lines.marker'] = marker
        plt.rcParams['lines.markeredgecolor'] = markeredgecolor
        plt.rcParams['lines.markeredgewidth'] = markeredgewidth
        plt.rcParams['lines.markerfacecolor'] = markerfacecolor
        plt.rcParams['lines.markersize'] = markersize
    def show_bar_values(bars: BarContainer, fontsize: int = 12, color: str = "black", padding: int | float = 0) -> BarContainer:
        """
        This function adds text labels to the bars in a bar plot, displaying the actual height of each bar.

        Parameters:
        bars (BarContainer): The BarContainer object returned by the bar plot function.
        fontsize (int): The size of the text labels. Default is 12.
        color (str): The color of the text labels. Default is "black".
        padding (int | float): The padding between the bar and the text label. Default is 0.

        Returns:
        BarContainer: The same BarContainer object with added text labels.
        """
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2.0, height + padding, f'{height}', ha='center', va='bottom', fontsize=fontsize, color=color)
        return bars
    def highlight_equal_values(bars: BarContainer, facecolor: str = "orange", edgecolor: str = "black", linewidth: int | float = 2, alpha: int | float = 1) -> BarContainer:
        """
        This function highlights bars with equal heights in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        facecolor (str): The color to fill the highlighted bars. Default is "orange".
        edgecolor (str): The color of the edges of the highlighted bars. Default is "black".
        linewidth (int | float): The width of the edges of the highlighted bars. Default is 2.
        alpha (int | float): The transparency of the highlighted bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with highlighted bars.
        """
        height_to_indices = {}
        for index, bar in enumerate(bars):
            height = bar.get_height()
            if height not in height_to_indices:
                height_to_indices[height] = []
            height_to_indices[height].append(index)
        indices_with_same_value = [indices for indices in height_to_indices.values() if len(indices) > 1]
        flat_indices_with_same_value = [index for sublist in indices_with_same_value for index in sublist]
        for i in flat_indices_with_same_value:
            bars[i].set_color(facecolor)
            bars[i].set_edgecolor(edgecolor)
            bars[i].set_linewidth(linewidth)
            bars[i].set_alpha(alpha)
        return bars
    def change_bar_colors(bars: BarContainer, facecolors: list[str]= ["yellow"], edgecolors: list[str] = ["black"], linewidth: int | float = 2, alpha: int | float = 1)-> BarContainer:
        """
        This function changes the colors of bars in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the plot.
        facecolors (list[str]): A list of colors for the face of the bars. Default is ["yellow"].
        edgecolors (list[str]): A list of colors for the edges of the bars. Default is ["black"].
        linewidth (int | float): The width of the bar edges. Default is 2.
        alpha (int | float): The transparency of the bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with updated colors.
        """
        # Create cyclic iterators for facecolors and edgecolors
        facecolors_cycle = itertools.cycle(facecolors)
        edgecolors_cycle = itertools.cycle(edgecolors)

        # Iterate over each bar, facecolor, and edgecolor
        for bar, facecolor, edgecolor in zip(bars, facecolors_cycle, edgecolors_cycle):
            # Set the color, edgecolor, linewidth, and alpha of the bar
            bar.set_color(facecolor)
            bar.set_edgecolor(edgecolor)
            bar.set_linewidth(linewidth)
            bar.set_alpha(alpha)

        # Return the modified bars
        return bars
    def highlight_max_min_bar(bars: BarContainer, max_facecolor: str | tuple = 'green', max_edgecolor: str | tuple = 'black', max_linewidth: int | float = 2, min_facecolor: str | tuple = 'red', min_edgecolor: str | tuple = 'black', min_linewidth: int | float = 2, alpha: int | float = 1)-> BarContainer:
        """
        This function highlights the maximum and minimum bars in a bar plot.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        max_facecolor (str | tuple): The color of the maximum bar face. Default is 'green'.
        max_edgecolor (str | tuple): The color of the maximum bar edge. Default is 'black'.
        max_linewidth (int | float): The width of the maximum bar edge. Default is 2.
        min_facecolor (str | tuple): The color of the minimum bar face. Default is 'red'.
        min_edgecolor (str | tuple): The color of the minimum bar edge. Default is 'black'.
        min_linewidth (int | float): The width of the minimum bar edge. Default is 2.
        alpha (int | float): The transparency of the bars. Default is 1.

        Returns:
        BarContainer: The modified container of bars with highlighted maximum and minimum bars.
        """
        heights = [bar.get_height() for bar in bars]
        min_height = np.min(heights)
        max_height = np.max(heights)
        for bar in bars:
            if bar.get_height() == min_height:        
                bar.set_color(min_facecolor)
                bar.set_edgecolor(min_edgecolor)
                bar.set_linewidth(min_linewidth)
                bar.set_alpha(alpha)
            if bar.get_height() == max_height:
                bar.set_color(max_facecolor)
                bar.set_edgecolor(max_edgecolor)
                bar.set_linewidth(max_linewidth)
                bar.set_alpha(alpha)
        return bars
    def hightlight_median(bars: BarContainer, facecolor: str = "purple", edgecolor: str = "black", linewidth: int | float = 2, alpha: int | float = 1) -> BarContainer:
        """
        Highlights the median bar in a bar plot by changing its color, edge color, line width, and transparency.

        Parameters:
        bars (BarContainer): The container of bars in the bar plot.
        facecolor (str): The color of the median bar. Default is "purple".
        edgecolor (str): The color of the edge of the median bar. Default is "black".
        linewidth (int | float): The width of the line of the median bar. Default is 2.
        alpha (int | float): The transparency of the median bar. Default is 1.

        Returns:
        BarContainer: The modified container of bars with the highlighted median bar.
        """
        heights = [bar.get_height() for bar in bars]
        median_height = np.median(heights)
        median_index = np.argmin(np.abs(np.array(heights) - median_height))
        bars[median_index].set_color(facecolor)
        bars[median_index].set_edgecolor(edgecolor)
        bars[median_index].set_linewidth(linewidth)
        bars[median_index].set_alpha(alpha)
        return bars
            
def read_file(path: str, **kwargs) -> xr.Dataset | pd.DataFrame:
    """
    Reads a file from the given path and returns the data in a structured format.

    Args:
        path (str): The path to the file to be read.
        kwargs: Additional options to customize the file reading process.

    Returns:
        File object or list of tables: The data from the file in a structured format, except for HTML files where a list of tables is returned.

    Raises:
        ValueError: If the given path is not a valid file or the file format is not supported.
        RuntimeError: If there is an error in reading the file.
    """
    # Check if the given path is a file
    if not os.path.isfile(path):
        # Raise a ValueError if the path is not a file
        raise ValueError("Invalid file path.")

    try:
        # Get the file extension
        extension = Settings.get_file_extension(path)
        # If the extension is .csv, read the file as a CSV
        if extension == ".csv":
            df = pd.read_csv(path, **kwargs)
        # If the extension is .parquet, read the file as a Parquet
        elif extension == ".parquet":
            metadata_dict = {}
            parquet_file = pq.ParquetFile(path)
            schema = parquet_file.schema_arrow
            for field in schema:
                if field.metadata:
                    metadata_dict[field.name] = {
                        k.decode('utf-8'): v.decode('utf-8') for k, v in field.metadata.items()
                    }

            # Read the Parquet file into a pandas DataFrame
            df = pd.read_parquet(path, **kwargs)
            # Attach metadata to the DataFrame
            df.attrs['metadata'] = metadata_dict
        # If the extension is .json, read the file as a JSON
        elif extension == ".json":
            df = pd.read_json(path, **kwargs)
        # If the extension is .xlsx, read the file as an Excel file
        elif extension == ".xlsx":
            df = pd.read_excel(path, **kwargs)
        # If the extension is .xml, read the file as an XML
        elif extension == ".xml":
            df = pd.read_xml(path, **kwargs)
        # If the extension is .feather, read the file as a Feather file
        elif extension == ".feather":
            df = pd.read_feather(path, **kwargs)
        # If the extension is .html, read the file as HTML
        elif extension == ".html":
            df = pd.read_html(path, **kwargs)
        # If the extension is .nc, read the file as a NetCDF file
        elif extension == ".nc":
            df = xr.open_dataset(path, **kwargs)
        # Raise a ValueError if the extension is not supported
        else:
            raise ValueError(f"Unsupported file format for {path}. Supported formats: CSV, Parquet, JSON, Excel, XML, Feather, and NetCDF.")
        return df
    except Exception as e:
        # Raise a RuntimeError if there is an error reading the file
        raise RuntimeError(f"Error in reading the file {path}: {e}")
    
def start_Cleaning(self) -> Cleaning:
    """
    This function initializes and returns an instance of the Cleaning class.

    Parameters:
    self (object): The current instance of the class or function.

    Returns:
    cleaning (Cleaning): An instance of the Cleaning class.
    """
    cleaning = Cleaning(self)
    return cleaning
def start_Optimization(self) -> Optimization:
    """
    This function initializes and returns an instance of the Optimization class.

    Parameters:
    self (object): The current instance of the class or function.

    Returns:
    optimization (Optimization): An instance of the Optimization class.
    """
    optimization = Optimization(self)
    return optimization
def start_Statistics(self) -> Statistics:
    """
    This function initializes and returns an instance of the Statistics class.

    Parameters:
    self (object): The current instance of the class or function.

    Returns:
    statistics (Statistics): An instance of the Statistics class.
    """
    statistics = Statistics(self)
    return statistics
def start_netCDFMetadata(self) -> netCDFMetadata:
    """
    This function initializes and returns an instance of the netCDFMetadata class.

    Parameters:
    self (object): The current instance of the class or function. This parameter is used to pass the current context or data to the netCDFMetadata class.

    Returns:
    net_cdf_metadata (netCDFMetadata): An instance of the netCDFMetadata class. This instance can be used to perform operations related to netCDF metadata.

    Raises:
    None
    """
    net_cdf_metadata = netCDFMetadata(self)
    return net_cdf_metadata
def start_ParquetMetadata(self) -> ParquetMetadata:
    """
    This function initializes and returns an instance of the ParquetMetadata class.

    Parameters:
    self (object): The current instance of the class or function. This parameter is used to pass the current context or data to the ParquetMetadata class.

    Returns:
    parquetmetadata (ParquetMetadata): An instance of the ParquetMetadata class. This instance can be used to perform operations related to Parquet metadata.

    Raises:
    None
    """
    metadata = self.attrs.get("metadata") if "metadata" in self.attrs else None
    columns = self.columns
    dtypes = self.dtypes
    parquetmetadata = ParquetMetadata(self, metadata, columns, dtypes)
    return parquetmetadata
def start_Visualization(self) -> Visualization:
    """
    This function initializes and returns an instance of the Visualization class.

    Parameters:
    self (object): The current instance of the class or function. This parameter is used to pass the current context or data to the Visualization class.

    Returns:
    visualization (Visualization): An instance of the Visualization class. This instance can be used to perform operations related to data visualization.

    Raises:
    None
    """
    visualization = Visualization(self)
    return visualization
def change_Settings() -> Settings:
    """
    This function returns an instance of the Settings class.

    Returns:
    Settings: An instance of the Settings class. This instance can be used to access and modify various settings related to data analysis and visualization.
    """
    return Settings