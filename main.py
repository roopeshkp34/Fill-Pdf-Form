import calendar
import datetime, enum
from typing import List
from fastapi import FastAPI, Form, HTTPException, status
from fastapi.responses import FileResponse
import uvicorn
from fillpdf import fillpdfs

app = FastAPI()


class FavoriteActivity(str, enum.Enum):
    READING: str = "Reading"
    WALKING: str = "Walking"
    MUSIC: str = "Music"
    OTHER: str = "Other"


ACTIVITY_CHECK_BOX_DICT = {
    "Reading": "Check Box1",
    "Walking": "Check Box2",
    "Music": "Check Box3",
    "Other": "Check Box4",
}


def month_number_to_abbr(month_number: int) -> str:
    """
    Convert a month number to its corresponding three-letter abbreviation.
    
    Args:
        month_number (int): The month number (1 for January, 2 for February, ..., 12 for December).

    Returns:
        str: The three-letter abbreviation of the month.
    """
    if 1 <= month_number <= 12:
        return calendar.month_abbr[month_number]
    else:
        raise ValueError("Month number must be between 1 and 12")


@app.post("/fill-pdf")
def fill_pdf(
    name: str = Form(...),
    date: datetime.date = Form(...),
    address: str = Form(...),
    favorite_activities_checkbox: List[str] = Form(...),
    favorite_activity_radio: FavoriteActivity = Form(...),
):
    try:
        # Convert list of string activities to list of Activity enums
        favorite_activities_checkbox: List[FavoriteActivity] = [
            FavoriteActivity(activity)
            for activity in favorite_activities_checkbox[0].split(",")
            if activity in FavoriteActivity.__members__.values()
        ]

        data_dict = {
            "Name": name,
            "Address": address,
            "Dropdown1": int(date.day),
            "Dropdown2": month_number_to_abbr(date.month),
            "Dropdown3": date.year,
            "Group6": list(FavoriteActivity).index(FavoriteActivity(favorite_activity_radio)),
        }
        for activity in favorite_activities_checkbox:
            if activity.value in ACTIVITY_CHECK_BOX_DICT:
                data_dict.update({ACTIVITY_CHECK_BOX_DICT[activity.value]: "Yes"})

        output_path: str = "filled_form.pdf"
        fillpdfs.write_fillable_pdf(
            "sample_pdf.pdf", output_pdf_path=output_path, data_dict=data_dict, flatten=True
        )
        return FileResponse(output_path, filename="filled_form.pdf")
    except KeyError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Input form data is not valid.")
    except Exception:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Failed to fill pdf form.")



if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
