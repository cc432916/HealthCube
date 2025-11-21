from datetime import datetime
import json
import os
from typing import List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

router = APIRouter(prefix="/api/user", tags=["user-data"])

DATA_FILE = "user_body_data.json"


class BodyRecordInput(BaseModel):
    weight: float = Field(..., description="kg")
    height: float = Field(..., description="cm")
    chest: Optional[float] = None
    waist: Optional[float] = None
    hip: Optional[float] = None
    body_fat: Optional[float] = None
    gender: str
    age: int


class BodyRecord(BodyRecordInput):
    id: int
    date: str
    time: str
    bmi: float
    whr: Optional[float] = None


class HistoryResponse(BaseModel):
    records: List[BodyRecord]


def _load_records() -> List[dict]:
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_records(records: List[dict]) -> None:
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)


@router.post("/body-data", response_model=BodyRecord)
def save_body_data(data: BodyRecordInput):
    records = _load_records()
    new_id = records[-1]["id"] + 1 if records else 1

    bmi = round(data.weight / ((data.height / 100) ** 2), 1)
    whr = None
    if data.waist and data.hip:
        whr = round(data.waist / data.hip, 2)

    now = datetime.now()
    rec = {
        "id": new_id,
        "date": now.date().isoformat(),
        "time": now.strftime("%H:%M"),
        "weight": data.weight,
        "height": data.height,
        "chest": data.chest,
        "waist": data.waist,
        "hip": data.hip,
        "body_fat": data.body_fat,
        "gender": data.gender,
        "age": data.age,
        "bmi": bmi,
        "whr": whr,
    }
    records.append(rec)
    _save_records(records)
    return rec


@router.get("/body-data/history", response_model=HistoryResponse)
def get_history():
    records = _load_records()
    return {"records": records}


@router.delete("/body-data/{record_id}")
def delete_record(record_id: int):
    records = _load_records()
    new_records = [r for r in records if r["id"] != record_id]
    if len(new_records) == len(records):
        raise HTTPException(status_code=404, detail="记录不存在")
    _save_records(new_records)
    return {"ok": True}
