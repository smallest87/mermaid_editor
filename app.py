from core.engine import MermaidEngine


def run_test():
    engine = MermaidEngine()

    print("[1] Menambahkan Node Utama...")
    engine.add_node("START", "Input Data", shape="circle")
    engine.add_node("PROCESS", "Validasi", shape="diamond")
    engine.add_node("END", "Sukses", shape="rect")

    print("[2] Menambahkan Garis dengan Belokan...")
    # Tanpa belokan
    engine.connect_with_routing("START", "PROCESS", waypoints=0)
    # Dengan 2 belokan (helper nodes)
    engine.connect_with_routing("PROCESS", "END", waypoints=2, label="Valid")

    print("\n--- HASIL GENERASI KODE MERMAID ---")
    print(engine.get_mermaid_string())

    print("\n[3] Mengekspor ke JSON...")
    # Menggunakan model_dump_json() untuk Pydantic v2
    with open("output_state.json", "w") as f:
        f.write(engine.state.model_dump_json(indent=4))
    print("File 'output_state.json' berhasil dibuat.")


if __name__ == "__main__":
    run_test()
