package competition;
public enum PitchType {
	AG("artifical-grass"),
	FG("field-grass"),
	DIRT("dirt");
	
	private final String typeName;
	
	private PitchType(String typeName) {
		this.typeName = typeName;
	}
	
	public String toString() {
		return this.typeName;
	}
}