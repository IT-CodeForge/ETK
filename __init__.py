from .Internal.ETKEventData import ETKEventData
from .Internal.ETKBaseObject import ETKBaseObject
from .Internal.ETKBaseWidget import ETKBaseWidget
from .Internal.ETKBaseTkObject import ETKBaseTkObject
from .Internal.ETKBaseTkWidget import ETKBaseTkWidget, ETKBaseWidget
from .Internal.ETKBaseWidgetDisableable import ETKBaseWidgetDisableable
from .Internal.ETKBaseTkWidgetDisableable import ETKBaseTkWidgetDisableable
from .Internal.ETKBaseTkWidgetText import ETKBaseTkWidgetText
from .ETKBitmap import ETKBitmap
from .ETKButton import ETKButton
from .ETKCanvas import ETKCanvas
from .ETKCanvasCircle import ETKCanvasCircle
from .ETKCanvasItem import ETKCanvasItem
from .ETKCanvasLine import ETKCanvasLine
from .ETKCanvasOval import ETKCanvasOval
from .ETKCanvasRectangle import ETKCanvasRectangle
from .ETKCanvasSquare import ETKCanvasSquare
from .ETKCheckbox import ETKCheckbox
from .Internal.ETKBaseContainer import ETKBaseContainer
from .ETKContainer import ETKContainer
from .ETKEdit import ETKEdit
from .ETKLabel import ETKLabel
from .ETKListingContainer import ETKListingContainer
from .ETKMainWindow import ETKMainWindow
from .ETKTimer import ETKTimer
from .Vector2d import Vector2d
from .ETKDropdownMenu import ETKDropdownMenu

if __name__ == "__main__":
    # Alles importierte wird einmal verwendet, damit keine "WirdNichtVerwendet" Warnung getriggert wird.
    ETKBitmap.abs_enabled
    ETKButton.abs_enabled
    ETKCanvas.abs_enabled
    ETKCanvasCircle.background_color
    ETKCanvasItem.background_color
    ETKCanvasLine.background_color
    ETKCanvasOval.background_color
    ETKCanvasRectangle.background_color
    ETKCanvasSquare.background_color
    ETKCheckbox.abs_enabled
    ETKContainer.abs_enabled
    ETKEdit.abs_enabled
    ETKLabel.abs_enabled
    ETKListingContainer.abs_enabled
    ETKMainWindow.abs_pos
    ETKTimer.mro
    Vector2d.mro
    ETKDropdownMenu.abs_enabled
    ETKBaseContainer.abs_enabled
    ETKBaseObject.abs_pos
    ETKBaseWidget.abs_enabled
    ETKBaseTkObject.abs_pos
    ETKBaseTkWidget.abs_enabled
    ETKBaseWidgetDisableable.abs_enabled
    ETKBaseTkWidgetDisableable.abs_enabled
    ETKBaseTkWidgetText.abs_enabled
    ETKEventData.__annotations__