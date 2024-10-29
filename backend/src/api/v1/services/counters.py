from typing import List

from sqlalchemy.orm import Session
from sqlmodel import select

from src.database.schema import Counter
from src.models.counter import CounterPresentation


class CountersSevice:
    @staticmethod
    def get_counters(session: Session) -> List[CounterPresentation]:
        counters = session.execute(select(Counter)).scalars().all()
        return [
            CounterPresentation(
                endpoint_name=counter.endpoint_name,
                count=counter.count,
            )
            for counter in counters
        ]

    @staticmethod
    def increment_counter(session: Session, endpoint_name: str) -> Counter:
        counter = session.query(Counter).filter_by(endpoint_name=endpoint_name).first()

        if not counter:
            counter = Counter(endpoint_name=endpoint_name)

        counter.count += 1
        session.add(counter)
        session.commit()
        session.refresh(counter)

        return counter
