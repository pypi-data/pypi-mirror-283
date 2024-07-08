import os
import sqlite3
import uuid
from dataclasses import dataclass
from typing import List, Optional

from fabric import Connection

from .cluster_config import ClusterConfig


@dataclass
class Job:
    id: str
    name: str
    status: str
    working_dir: str
    nodes: List[str]
    cluster: str


class JobManager:
    def __init__(
        self, db_path: str = os.path.expanduser("~/.cache/torch-submit/jobs.db")
    ):
        self.conn = sqlite3.connect(db_path)
        self.create_table()

    def create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                working_dir TEXT,
                nodes TEXT,
                cluster TEXT
            )
        """)

    def add_job(self, job: Job):
        self.conn.execute(
            """
            INSERT INTO jobs (id, name, status, working_dir, nodes, cluster)
            VALUES (?, ?, ?, ?, ?, ?)
        """,
            (
                job.id,
                job.name,
                job.status,
                job.working_dir,
                ",".join(job.nodes),
                job.cluster,
            ),
        )
        self.conn.commit()

    def get_job(self, job_id: str) -> Optional[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        if row:
            return Job(
                id=row[0],
                name=row[1],
                status=row[2],
                working_dir=row[3],
                nodes=row[4].split(","),
                cluster=row[5],
            )
        return None

    def list_jobs(self) -> List[Job]:
        cursor = self.conn.execute("SELECT * FROM jobs")
        return [
            Job(
                id=row[0],
                name=row[1],
                status=row[2],
                working_dir=row[3],
                nodes=row[4].split(","),
                cluster=row[5],
            )
            for row in cursor.fetchall()
        ]
    
    def check_job_status(self, job: Job, cluster_config: ClusterConfig) -> str:
        script_name = job.command.split()[-1]
        script_path = os.path.join(f"/tmp/torch_submit_job_{job.id}", script_name)
        cluster = cluster_config.get_cluster(job.cluster)
        
        for node in [cluster.head_node] + cluster.worker_nodes:
            node_ip = node.private_ip or node.public_ip
            try:
                with Connection(node_ip, connect_timeout=5) as c:
                    result = c.run(f"pgrep -f '{script_path}'", warn=True, hide=True)
                    if result.ok:
                        return "running"
            except Exception:
                # If we can't connect to a node, we'll continue to the next one
                continue
        
        # If we've checked all nodes and found no running processes
        if job.status == "stopped":
            return "stopped"
        elif job.status == "started" or job.status == "running":
            return "crashed"
        else:
            return job.status  # Return the current status if it's not one we're updating

    def get_all_jobs_with_status(self, cluster_config: ClusterConfig) -> List[Job]:
        jobs = self.list_jobs()
        for job in jobs:
            job.status = self.check_job_status(job, cluster_config)
        return jobs

    def update_job_status(self, job_id: str, status: str):
        self.conn.execute("UPDATE jobs SET status = ? WHERE id = ?", (status, job_id))
        self.conn.commit()

    def delete_job(self, job_id: str):
        self.conn.execute("DELETE FROM jobs WHERE id = ?", (job_id,))
        self.conn.commit()

    def close(self):
        self.conn.close()


def create_job(name: str, working_dir: str, nodes: List[str], cluster: str) -> Job:
    return Job(
        id=str(uuid.uuid4()),
        name=name,
        status="submitted",
        working_dir=working_dir,
        nodes=nodes,
        cluster=cluster,
    )
