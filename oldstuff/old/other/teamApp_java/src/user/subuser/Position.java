package user.subuser;
public enum Position {
	
	GK("goalkeeper"),
	CB("centre-back"),
	RB("right-back"),
	LB("left-back"),
	CM("centre-midfield"),
	RM("right-midfield"),
	LM("left-midfield"),
	RW("right-wing"),
	LW("left-wing"),
	ST("striker");
	
	private final String positionName;
	
	private Position(String positionName) {
		this.positionName = positionName;
	}
	
	public String toString() {
		return this.positionName;
	}
}